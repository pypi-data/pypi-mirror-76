class logger:
    """
    Concept: Lean Waterfall Process
    Inspired by: 
    (1) adina's idea to output the waterfall as a pandas df 
    (instead of going back and forth sa doc / sheet! efficient!!!!)
    (2) pandas-logger package
    (3) towardsdatascience.com/the-unreasonable-effectiveness-of-method-chaining-in-pandas-15c2109e3c69
    """
    def __init__(self, echo, *functions):
        self.f_set = functions
        self.result = {}
        self.counter = 0 # can't remember why there's a counter
        self.echo = echo
        print("Logger created.")

    def log(self, df, statement = None):
        
        if statement is None:
            statement = "Step {}".format(self.counter)
        self.result[statement] = {}
        
        if self.echo == True:
            print("-------")
            print(statement)
        for f in self.f_set:
            temp = f(df)
            self.result[statement][f.__name__] = temp
            if self.echo == True:
                print(f.__name__, ":", temp)
            
            self.counter = self.counter + 1 # can't remember why there's a counter
        return df.copy()

    def getResults(self):
        return pd.DataFrame.from_dict(self.result, orient = "index")