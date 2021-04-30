class Echo:
    name = "Narcissus"
    def __getattr__(self, item):
        def echo():
            print(item + self.name)
        return echo


e = Echo()
e.hello()