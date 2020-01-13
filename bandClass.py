class Bandaid:
    def __init__(self, apiResult, postsCount, adminCount, commentCount, memberCount, adminActivity, totalActivity):
        self.apiResult = apiResult
        self.postsCount = postsCount
        self.adminCount = adminCount
        self.commentCount = commentCount
        self.memberCount = memberCount
        self.totalActivity = adminActivity
        self.adminActivity = totalActivity

    # def get_totalActivity(self):
    #     return self.__x

    # def set_totalActivity(self, x):
    #     self.__x = x

    # def get_adminActivity(self):
    #     return self.__x

    # def set_adminActivity(self, x):
    #     self.__x = x
