"""Simplified mattermost interface."""
from exceptions import ConfigError
import requests
import mattermostdriver
from dtos import PostDTO
from doi import Doi


class Mattermost:
    """Provide a simplified interaction w/ mattermost api."""
    def __init__(self, url, channelname, username, password):
        self.msgs = []
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
        """Try to find the paper channel by display name."""
        teamapi = self.mattermost.teams
        channelapi = self.mattermost.channels
        teams = [team["id"] for team in teamapi.get_user_teams("me")]
        channels = []
        for team in teams:
            teamchannels = [channel for channel
                            in channelapi.get_channels_for_user("me", team)
                            if channel["display_name"] == channelname]
            channels.extend(teamchannels)

        # lets just hope no-one has the same channel name in multiple teams
        if len(channels) == 0:
            print(f"Channel {channelname} does not exits")
            raise ConfigError
        return channels[0]["id"]

    def get_reporter(self, userid):
        """Load user from mattermost api and cache."""
        userapi = self.mattermost.users
        if userid not in self.reporters:
            self.reporters[userid] = userapi.get_user(userid)["username"]

        return self.reporters[userid]

    def retrieve_all_messages(self):
        """Retrieve all messages from mattermost, unfiltered for papers."""
        posts = self.mattermost.posts.get_posts_for_channel(self.channel)
        return [PostDTO(id=m['id'], message=m['message'],
                        reporter=self.get_reporter(m['user_id']),
                        doi=Doi().extract_doi(m['message']),)
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
        """Check for doi in current paper list."""
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
        """Post message to thread."""
        self.mattermost.posts.create_post({"channel_id": self.channel,
                                           "message": message})
