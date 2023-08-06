""""Paper surfer - browse papers posted on the mattermost channel.

UI:

[____(filter)______]
1. paper (open discussion) (open paper)
2. paper (open discussion) (open paper)
3. paper (open discussion) (open paper)
4. paper (open discussion) (open paper)

"""
import subprocess
from dataclasses import dataclass
import re
from functools import partial
import json
import time
import os
import requests
import mattermostdriver
import urwid
import configargparse


class ConfigError(Exception):
    """Configuration error."""


@dataclass
class PostDTO:
    """"Encapsulate Mattermost Posts."""
    id: str
    message: str
    reporter: str
    doi: str

    def __str__(self):
        return self.message


@dataclass
class PaperDTO:
    """"Encapsulate Paper meta data."""
    author: str
    authors: str
    title: str
    journal: str
    year: int
    abstract: str
    doi: str
    slug: str


class Bibtex:
    def entry_from_doi(self, doi):
        return Doi().get_bibtex(doi)

    def bib_from_dois(self, dois):
        return "\n".join([Doi().get_bibtex(doi) for doi in dois])


class Doi:
    """Interface w/ the doi.org api"""
    def get_doi_link(self, doi):
        """Assemble doi link."""
        return f"http://doi.org/{doi}"

    def load_doi_data(self, doi):
        headers = {
            'Accept': 'application/json',
        }
        return requests.get(f'http://dx.doi.org/{doi}',
                            headers=headers).content

    def parse_doi_json(self, jsoncontent):
        """Tranform doi json to PaperDTO"""
        info = json.loads(jsoncontent)

        with open("debug.json", "w") as file:
            file.write(json.dumps(info))

        author = (f"{info['author'][0]['given']} {info['author'][0]['family']}"
                  if "author" in info
                  else "Author N/A")
        authors = (", ".join([f"{a['given']} {a['family']}"
                              for a in info['author']])
                   if "author" in info
                   else "Authors N/A")
        title = (info['title']
                 if "title" in info
                    and isinstance(info['title'], str)
                 else "Title N/A")
        journal = (info['publisher']
                   if "publisher" in info
                   else "Journal N/A")
        year = info['created']['date-parts'][0][0]
        doi = info['DOI']
        abstract = (info['abstract']
                    if "abstract" in info
                    else "Abstract N/A")

        slug = f"{info['author'][0]['family']}{year}"

        return PaperDTO(author, authors, title, journal, year, abstract, doi,
                        slug)

    def get_bibtex(self, doi):
        headers = {
            'Accept': 'text/bibliography; style=bibtex',
        }
        return requests.get(f'http://dx.doi.org/{doi}', headers=headers).text

    def get_info(self, doi):
        try:
            jsoncontent = self.load_doi_data(doi)
            data = self.parse_doi_json(jsoncontent)
            return data
        except json.decoder.JSONDecodeError:
            return None

    def extract_doi(self, hay):
        """Parse doi from string, or None if not found.

        >>> Doi().extract_doi("https://doi.org/10.1093/petrology/egaa077")
        '10.1093/petrology/egaa077'
        """
        pattern = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+'
        matches = re.compile(pattern, re.I).search(hay)
        return matches.group() if matches else None


class Mattermost:
    """Provide a simplified interaction w/ mattermost api."""
    def __init__(self, url, channelname, username, password):
        self.mattermost = mattermostdriver.Driver({
            'url': url,
            'login_id': username,
            'password': password,
            'port': 443
        })

        try:
            self.mattermost.login()
        except (mattermostdriver.exceptions.NoAccessTokenProvided,
                requests.exceptions.InvalidURL,
                requests.exceptions.HTTPError):
            print("Failed to log into Mattermost.")
            raise ConfigError

        try:
            self.channel = self.get_channel(channelname)
        except ConfigError:
            print("Couldn't find Mattermost channel.")
            raise ConfigError
        self.reporters = {}

    def get_channel(self, channelname):
        """"Try to find the paper channel by display name."""
        mm = self.mattermost
        teams = [team["id"] for team in mm.teams.get_user_teams("me")]
        channels = []
        for team in teams:
            teamchannels = [channel for channel
                            in mm.channels.get_channels_for_user("me", team)
                            if channel["display_name"] == channelname]
            channels.extend(teamchannels)

        # lets just hope no-one has the same channel name in multiple teams
        if len(channels) == 0:
            print(f"Channel {channelname} does not exits")
            raise ConfigError
        return channels[0]["id"]

    def get_reporter(self, id):
        """Load user from mattermost api and cache."""
        if id not in self.reporters:
            self.reporters[id] = self.mattermost.users.get_user(id)["username"]

        return self.reporters[id]

    def retrieve_all_messages(self):
        """Retrieve all messages from mattermost, unfiltered for papers."""
        posts = self.mattermost.posts.get_posts_for_channel(self.channel)
        return [PostDTO(
                    id=m['id'],
                    message=m['message'],
                    reporter=self.get_reporter(m['user_id']),
                    doi=Doi().extract_doi(m['message']),
                )
                for m in posts['posts'].values()]

    def filter_incoming(self, posts):
        """Filter messages from mattermost to only papers."""
        return [p for p in posts if "doi" in p.message]

    def retrieve(self):
        """Retrieve papers from mattermost channel."""
        msgs = self.retrieve_all_messages()
        self.msgs = self.filter_incoming(msgs)
        return self.msgs

    def check_doi_exits(self, doi):
        doi_needle = Doi().extract_doi(doi)
        msg_found = [msg for msg in self.msgs
                     if Doi().extract_doi(msg.doi) == doi_needle]
        return bool(msg_found)

    def get_filtered(self, needle):
        """Filter posts by needle."""
        return [m for m in self.msgs
                if needle.lower() in m.message.lower()
                or needle.lower() in m.reporter.lower()]

    def post(self, message):
        self.mattermost.posts.create_post({"channel_id": self.channel,
                                           "message": message})


class PrettyButton(urwid.WidgetWrap):
    def __init__(self, label, on_press=None, user_data=None):
        self.text = urwid.Text("")
        self.set_label(label)
        self.widget = urwid.AttrMap(self.text, '', 'highlight')

        # use a hidden button for evt handling
        self._hidden_btn = urwid.Button(f"hidden {self.label}",
                                        on_press, user_data)

        super(self.__class__, self).__init__(self.widget)

    def selectable(self):
        return True

    def keypress(self, *args, **kw):
        return self._hidden_btn.keypress(*args, **kw)

    def mouse_event(self, *args, **kw):
        return self._hidden_btn.mouse_event(*args, **kw)

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label
        self.text.set_text(f"[ {label} ]")


class Papersurfer:
    """Provide UI and interface with mattermost class."""

    _palette = [
        ('button', 'default,bold', 'default'),
        ('I say', 'default,bold', 'default', 'bold'),
        ('needle', 'default, bold, underline', 'default', 'bold'),
        ('highlight', 'black', 'dark blue'),
        ('banner', 'black', 'light gray'),
        ('selectable', 'white', 'black'),
        ('focus', 'black', 'light gray'),
        ('papertitle', 'default,bold', 'default', 'bold')
    ]

    def __init__(self, url, channel, username, password):
        self._screen = urwid.raw_display.Screen()
        self.size = self._screen.get_cols_rows()
        self.filter = ""

        ask = urwid.Edit(('I say', u"Filter?\n"))
        exitbutton = PrettyButton(u'Exit', on_press=self.on_exit_clicked)
        self.exportbutton = PrettyButton(u'Export filtered list as bibtex',
                                         on_press=self.on_export_clicked)
        submitbutton = PrettyButton('Submit paper',
                                    on_press=self.open_submit_paper)
        div = urwid.Divider(u'-')

        self.mtm = Mattermost(url, channel, username, password)

        body = [urwid.Text("")]
        self.listcontent = urwid.SimpleFocusListWalker(body)

        paperlist = urwid.BoxAdapter(urwid.ListBox(self.listcontent),
                                     self.size[1] - 5)
        buttonrow = urwid.Columns([exitbutton, self.exportbutton,
                                   submitbutton])
        self.pile = urwid.Pile([ask,
                                div,
                                paperlist,
                                div,
                                buttonrow])
        self.top = urwid.Filler(self.pile, valign='middle')
        self._pile = urwid.Pile(
            [
                self.loading_indicator()
            ]
        )
        self._over = urwid.Overlay(
            self._pile,
            self.top,
            align='center',
            valign='middle',
            width=20,
            height=10
        )

        urwid.connect_signal(ask, 'change', self.onchange)
        self.mainloop = urwid.MainLoop(self._over, self._palette,
                                       unhandled_input=self.h_unhandled_input)
        self.mainloop.set_alarm_in(.1, self.load_list)
        self.mainloop.run()

    def h_unhandled_input(self, key):
        if key == "esc":
            raise urwid.ExitMainLoop()

    def load_list(self, _loop, _data):
        body = [self.list_item(paper) for paper in self.mtm.retrieve()]
        self.listcontent.clear()
        self.listcontent.extend(body)
        self.mainloop.widget = self.top

    def loading_indicator(self):
        body_text = urwid.Text("Loading...", align='center')
        body_filler = urwid.Filler(body_text, valign='middle')
        body_padding = urwid.Padding(
            body_filler,
            left=1,
            right=1
        )

        return urwid.Frame(body_padding)

    def details_popup(self, paper):
        header_text = urwid.Text(('banner', 'Paper details'), align='center')
        header = urwid.AttrMap(header_text, 'banner')

        body_pile = urwid.Pile([
            urwid.Text(("papertitle", paper.title)),
            urwid.Text(paper.authors),
            urwid.Text(paper.journal),
            urwid.Text(paper.doi),
            urwid.Text(paper.abstract),
            urwid.Text(" "),
            urwid.Text(Bibtex().entry_from_doi(paper.doi)),
        ])
        body_filler = urwid.Filler(body_pile, valign='top')
        body_padding = urwid.Padding(
            body_filler,
            left=1,
            right=1
        )
        body = urwid.LineBox(body_padding)

        # Footer
        footer = PrettyButton('Okay', self.h_close_dialog)
        footer = urwid.GridFlow([footer], 8, 1, 1, 'center')

        # Layout
        layout = urwid.Frame(
            body,
            header=header,
            footer=footer,
            focus_part='footer'
        )

        return layout

    def list_item(self, paper, needle=""):
        """Create highlighted text entry."""
        text_items = []
        needle = needle or "ßß"
        msg = f"{paper.message} ({paper.reporter})"
        needles = re.findall(needle, msg, flags=re.IGNORECASE)
        hay = re.split(needle, msg, flags=re.IGNORECASE)
        for i, item in enumerate(hay):
            text_items.append(item)
            if i < len(needles):
                text_items.append(('needle', needles[i]))

        title = urwid.Text(text_items)
        discuss_button = PrettyButton("Open Discussion",
                                      on_press=partial(self.h_open_discussion,
                                                       paper))
        doi_button = PrettyButton("Open DOI",
                                  on_press=partial(self.h_open_doi, paper))
        details_button = PrettyButton("Show details",
                                      on_press=partial(self.h_show_details,
                                                       paper))

        button_bar = urwid.Columns([
            discuss_button, doi_button, details_button])
        pile = urwid.Pile([title, button_bar, urwid.Divider()])
        return pile

    def updscrn(self):
        """"Update (redraw) screen."""
        self.mainloop.draw_screen()

    def onchange(self, _, needle):
        """Handle filter change."""
        self.filter = needle
        self.listcontent.clear()
        self.listcontent.extend([self.list_item(paper, needle)
                                 for paper in self.mtm.get_filtered(needle)])

    def running_export(self, state):
        btn = self.exportbutton
        label = btn.get_label()
        running_indicator = " (running...)"
        if state:
            btn.set_label(label + running_indicator)
        else:
            btn.set_label(label.replace(running_indicator, ""))
        self.updscrn()

    def on_exit_clicked(self, button):
        """Handle exitbutton click and exit."""
        raise urwid.ExitMainLoop()

    def on_export_clicked(self, _):
        """Handle exitbutton click and exit."""
        self.running_export(True)
        self.export_to_bibtex()
        self.running_export(False)

    def export_to_bibtex(self):
        papers = self.mtm.get_filtered(self.filter)
        dois = [paper.doi for paper in papers]
        string = Bibtex().bib_from_dois(dois)
        with open("export.bib", 'w') as file:
            file.write(string)

    def h_open_discussion(self, post, _):
        """Handle click/enter on discussion button."""
        self.open_discussion(post)

    def h_open_doi(self, post, _):
        """Handle click/enter on doi button."""
        self.open_doi(post)

    def h_show_details(self, post, _):
        """Handle click/enter on doi button."""
        self.show_details(post)

    def open_discussion(self, post):
        """Open Mattermost post in browser."""
        link = f"https://mattermost.cen.uni-hamburg.de/ifg/pl/{post.id}"
        subprocess.call(["xdg-open", link])

    def open_doi(self, post):
        """Open paper page in browser."""
        subprocess.call(["xdg-open", Doi().get_doi_link(post.doi)])

    def show_details(self, post):
        """Open paper page in browser."""
        paper = Doi().get_info(post.doi)
        self.mainloop.widget = self.details_popup(paper)

    def h_close_dialog(self, _):
        self.close_dialog()

    def close_dialog(self):
        self.mainloop.widget = self.top

    def open_submit_paper(self, _):

        self._pile = urwid.Pile(
            [
                PostDialog(self.mtm, close=self.h_close_dialog)
            ]
        )
        self._over = urwid.Overlay(
            self._pile,
            self.top,
            align='center',
            valign='middle',
            width=100,
            height=200
        )

        self.mainloop.widget = self._over


def get_config_file_paths():
    """Find, load and parse a config file.

    The first config file that is found is used, it is searched for (in
    this order), at:
     - config, if set (e.g. from the cli)
     - from the default source path (./configurations/gascamcontrol.conf)
     - home path
       - XDG_CONFIG_HOME/gascamcontrol/gascamcontrol.conf (linux only)
     - system path
       - XDG_CONFIG_DIRS/gascamcontrol/gascamcontrol.conf (linux only)

    >>> type(get_config_file_paths())
    <class 'list'>
    """

    env = os.environ
    xdg_home = None
    if 'XDG_CONFIG_HOME' in env:
        xdg_home = env['XDG_CONFIG_HOME']
    elif 'HOME' in env:
        xdg_home = env['HOME'] + '/.config'

    xdg_config_dirs = None
    if 'XDG_CONFIG_DIRS' in env:
        xdg_config_dirs = env['XDG_CONFIG_DIRS'].split(':')
    elif 'HOME' in env:
        xdg_config_dirs = ['/etc/xdg']

    default_filename = "papersurfer.conf"

    default_path = "./"
    paths = [default_path, xdg_home]
    paths.extend(xdg_config_dirs)
    return [os.path.join(p, default_filename) for p in paths if p]


def interactive_configuration():
    url = input("Mattermost URL (eg. mattermost.example.net): ")
    channel = input("Channel (eg. Paper Club): ")
    username = input("Username (same as mattermost login, "
                     "eg. JohnDoe@example.net): ")
    password = input("Password (same as mattermost login, eg. SuperSecret1): ")
    return url, channel, username, password


class PostDialog(urwid.WidgetWrap):
    """
    UI:
        DOI: [ _________________]
        Generated Message:
            "# # # #  # # # #"

        [Submit]       [Close]
    """
    def __init__(self, mattermost, close):
        self.mattermost = mattermost
        self.close = close
        self.doi_input = urwid.Edit("Doi: ")
        urwid.connect_signal(self.doi_input, 'change', self.h_input)
        self.doi_result = urwid.Text("")

        body_pile = urwid.Pile([
            self.doi_input,
            urwid.Divider(" "),
            self.doi_result,
            urwid.Divider(" "),
            urwid.Columns([
                PrettyButton("Close", self.close),
                PrettyButton("Submit", self.submit)
            ]),
        ])
        body_filler = urwid.Filler(body_pile, valign='top')
        body_padding = urwid.Padding(
            body_filler,
            left=1,
            right=1
        )
        body = urwid.LineBox(body_padding)
        frame = urwid.Frame(
                body,
                header=urwid.Text("Submit new paper to list"),
            )

        self.widget = frame

        super(self.__class__, self).__init__(self.widget)

    def submit(self, _):
        if not self.mattermost.check_doi_exits(self.doi):
            self.mattermost.post(self.msg)
        self.close(_)

    def create_mgs(self, paper):
        msg = f"""\
{paper.title}
{paper.authors}
{paper.journal} [{paper.slug}]
{Doi().get_doi_link(paper.doi)}"""
        return msg

    def h_input(self, _, doi):
        self.doi_result.set_text("... loading ...")
        self.doi = None
        self.msg = None

        if Doi().extract_doi(doi):
            paper = Doi().get_info(doi)
            if paper:
                if self.mattermost.check_doi_exits(doi):
                    self.doi_result.set_text(f"{self.create_mgs(paper)} \n"
                                             "-> Paper already posted! <-")
                else:
                    self.doi_result.set_text(self.create_mgs(paper))
                    self.doi = doi
                    self.msg = self.create_mgs(paper)
            return

        self.doi_result.set_text("invalid doi")


def parse_args():
    """Parse command line arguments and config file."""
    parser = configargparse.ArgParser()
    parser._default_config_files = get_config_file_paths()
    parser.add("-w", "--write-out-config-file",
               help="takes the current command line args and writes them out "
                    "to a config file at the given path",
               is_write_out_config_file_arg=True)
    parser.add('-c', '--my-config', required=False, is_config_file=True,
               help='config file path')
    parser.add('--url', required=False, help='Mattermost url')
    parser.add('--channel', required=False, help='Mattermost channel')
    parser.add('-u', '--username', required=False, help='Mattermost username')
    parser.add('-p', '--password', required=False, help='Mattermost password')
    parser.add('--dump-posts', action='store_true',
               help="Dump mattermost paper posts to stdout and exit")
    parser.add('--dump-bibtex', action='store_true',
               help="Dump mattermost paper posts to stdout and exit")
    options = parser.parse_args()

    if not options.url:
        start_interactive = input(
            "Could not load config file or read command line arguments, do you"
            " wish to start the interactive configuration assistant? (y/n) ")
        if start_interactive == "y":
            url, channel, username, password = interactive_configuration()
            try:
                Mattermost(url, channel, username, password)
            except ConfigError:
                print("Failed to validate configuration, exiting.")
                exit(1)

            options.url = url
            options.channel = channel
            options.username = username
            options.password = password

            configfile = "papersurfer.conf"
            with open(configfile, "w") as file:
                file.write(f"url = {url}\n")
                file.write(f"channel = {channel}\n")
                file.write(f"username = {username}\n")
                file.write(f"password = {password}\n")
                print(f"Configfile {configfile} written.")

            time.sleep(2)
        else:
            parser.print_help()
            exit(0)

    return options


def just_papers(url, channel, username, password):
    """Fuck off with all this interactive shit."""
    posts = Mattermost(url, channel, username, password).retrieve()
    for post in posts:
        print(post)


def just_bibtex(url, channel, username, password):
    posts = Mattermost(url, channel, username, password).retrieve()
    dois = [post.doi for post in posts]
    print(Bibtex().bib_from_dois(dois))


def main():
    opt = parse_args()
    if opt.dump_posts:
        just_papers(opt.url, opt.channel, opt.username, opt.password)
    if opt.dump_bibtex:
        just_bibtex(opt.url, opt.channel, opt.username, opt.password)
    else:
        Papersurfer(opt.url, opt.channel, opt.username, opt.password)


if __name__ == "__main__":
    main()
