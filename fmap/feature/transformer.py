from nltk.stem.wordnet import WordNetLemmatizer
import re, time

class Transformer():
    def __init__(self):
        self.maps = []
        self.filters = []
        
        self.lemmatizr = WordNetLemmatizer()
        
        self.addDefaultOptions()
        
        self.techWords = ['', 'php', 'json', 'js']
        
        
    def transform(self, kws):
        for f in self.filters:
            kws = filter(f, kws)
        
        for m in self.maps:
            kws = map(m, kws)
            
        # Remove empty keywords
        kws = filter(lambda x: x!= '', kws)
          
        return kws
    
    def addDefaultOptions(self):
        # Filters
        # - token eliminator users numeric values in a word to detect tokens or hashes
        def tokenEliminator(word):
            m = re.findall('\d', word)
            if len(m) > 0: return False
            return True
        
        def emptyWordEliminator(word):
            if len(word) == 0: return False
            return True
        
        def longKeywordEliminator(word):
            if len(word) > 20: return False
            return True
        
        def techWordEliminator(word):
            if word in self.techWords: return False
            return True
        
        self.filters.extend([tokenEliminator, emptyWordEliminator, longKeywordEliminator, techWordEliminator])
        
        # Maps
        # - Lemmatizer
        def lemmatize(word): return self.lemmatizr.lemmatize(word)
        
        # - Composite query key simplification
        def queryKeySimplify(word):
            m = re.findall('\[\w*\]', word)
            if len(m) == 0: return word
            else: return m[len(m)-1][1:-1]
            
        self.maps.extend([lemmatize, queryKeySimplify])

    
    def addMap(self, m):
        self.maps.append(m)
    
    def addFilter(self, f):
        self.filters.append(f)
        
if __name__ == '__main__':
    t = Transformer()
    print t.transform(['foo1', 'sel[pass]', 'sessions', 'sdsd'])