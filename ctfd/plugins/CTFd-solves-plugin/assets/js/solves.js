const updateInterval = 300000;

Alpine.data('solves', () => ({
  challenges: [],
  teamStandings: [],
  userStandings: [],

  buildAccountUrl(accountType, accountId) {
    return `${CTFd.config.urlRoot}/admin/${accountType}/${accountId}`;
  },

  buildChallengeUrl(challengeId) {
    return `${CTFd.config.urlRoot}/admin/challenges/${challengeId}`;
  },

  update() {
    window.location.reload();
  },

  init(context) {
    if (!context) return;

    this.challenges = context.challenges ?? [];
    this.teamStandings = context.teamStandings ?? [];
    this.userStandings = context.userStandings ?? [];

    setInterval(() => {
      this.update();
    }, updateInterval);
  },
}));

Alpine.start();
