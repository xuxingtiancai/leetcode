class Solution:
    #KMP eigenvector
    def equal(self, char1, char2):
        return char1 == '?' or char2 == '?' or char1 == char2

    def getEigenvector(self, s):
        if s == '':
            return []
        num = [0] * len(s)
        for i in range(1, len(s)):
            k = num[i - 1]
            while not self.equal(s[i], s[k]) and k != 0:
                k = num[k - 1]
            if self.equal(s[i], s[k]):
                num[i] = k + 1
            else:
                num[i] = 0
        return num

    def kmp(self, string, pattern):
        if len(pattern) == 0:
            return 0
        if len(string) < len(pattern):
            return -1

        N = self.getEigenvector(pattern)
        j = 0
        for i in range(len(string)):
            while not self.equal(pattern[j], string[i]) and j > 0:
                j = N[j - 1]
            if self.equal(pattern[j], string[i]):
                j += 1
            if j == len(pattern):
                return i - j + 1
        return -1

    # @param s, an input string
    # @param p, a pattern string
    # @return a boolean
    def isMatch(self, string, pattern):
        subPatterns = re.split(r'\*+', pattern)

        sub = subPatterns[0]
        if not self.match_head(string, sub):
            return False
        string = string[len(sub) : ]
        if len(subPatterns) == 1:
            return string == ''

        for sub in subPatterns[1 : -1]:
            begin = self.kmp(string, sub)
            if begin == -1:
                return False
            string = string[begin + len(sub) : ]

        return self.match_tail(string, subPatterns[-1])

    def match_head(self, string, pattern):
        if len(string) < len(pattern):
            return False
        for s, p in zip(string, pattern):
            if not self.equal(s, p):
                return False
        return True

    def match_tail(self, string, pattern):
        if len(string) < len(pattern):
            return False
        for s, p in zip(string[::-1], pattern[::-1]):
            if not self.equal(s, p):
                return False
        return True
