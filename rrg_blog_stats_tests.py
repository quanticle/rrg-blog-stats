import unittest
from rrg_blog_stats import PostAnalyzer

class PostAnalyzerTests(unittest.TestCase):
    class StubbedPostAnalyzer(PostAnalyzer):
        def __init__(self):
            self.lines = []

    def testDateParsing_ValidDate(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append('title: "December 05 2016 RRG Notes"')
        meeting_date = post_analyzer.get_meeting_date()
        self.assertEqual(meeting_date.year, 2016)
        self.assertEqual(meeting_date.month, 12)
        self.assertEqual(meeting_date.day, 5)

    def testDateParsing_ValidSingleDigitDate(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append('title: "December 1 2016 RRG Notes"')
        meeting_date = post_analyzer.get_meeting_date()
        self.assertEqual(meeting_date.year, 2016)
        self.assertEqual(meeting_date.month, 12)
        self.assertEqual(meeting_date.day, 1)

    def testDateParsing_InvalidDate(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append('title: "This is not a date"')
        meeting_date = post_analyzer.get_meeting_date()
        self.assertEqual(meeting_date, None)

    def testGetArticleTitles_single_h3_title(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append("## Reading Notes")
        post_analyzer.lines.append("### [The Gervais Principle V: Heads I Win, Tails You Lose](http://www.ribbonfarm.com/2011/10/14/the-gervais-principle-v-heads-i-win-tails-you-lose/)")
        article_titles = post_analyzer.get_article_titles_and_urls()
        self.assertEqual(len(article_titles), 1)
        self.assertEqual(article_titles[0][0], "The Gervais Principle V: Heads I Win, Tails You Lose")
        self.assertEqual(article_titles[0][1], "http://www.ribbonfarm.com/2011/10/14/the-gervais-principle-v-heads-i-win-tails-you-lose/")

    def testGetArticleTitles_multiple_h3_titles(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append("## Reading Notes")
        post_analyzer.lines.append("### [The Gervais Principle V: Heads I Win, Tails You Lose](http://www.ribbonfarm.com/2011/10/14/the-gervais-principle-v-heads-i-win-tails-you-lose/)")
        post_analyzer.lines.append("* Hamartia - fatal error born of unavoidable ignorance")
        post_analyzer.lines.append("  * Concept from ancient Greece")
        post_analyzer.lines.append("### [The Gervais Principle Part VI: Children of an Absent God](http://www.ribbonfarm.com/2013/05/16/the-gervais-principle-vi-children-of-an-absent-god/)")
        article_titles = post_analyzer.get_article_titles_and_urls()
        self.assertEqual(len(article_titles), 2)
        self.assertEqual(article_titles[0][0], "The Gervais Principle V: Heads I Win, Tails You Lose")
        self.assertEqual(article_titles[0][1], "http://www.ribbonfarm.com/2011/10/14/the-gervais-principle-v-heads-i-win-tails-you-lose/")
        self.assertEqual(article_titles[1][0], "The Gervais Principle Part VI: Children of an Absent God")
        self.assertEqual(article_titles[1][1], "http://www.ribbonfarm.com/2013/05/16/the-gervais-principle-vi-children-of-an-absent-god/")

    def testGetArticleTitles_single_h2_title(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append("## [Living In An Inadequate World](https://equilibriabook.com/living-in-an-inadequate-world/)")
        article_titles = post_analyzer.get_article_titles_and_urls()
        self.assertEqual(len(article_titles), 1)
        self.assertEqual(article_titles[0][0], "Living In An Inadequate World")
        self.assertEqual(article_titles[0][1], "https://equilibriabook.com/living-in-an-inadequate-world/")

    def testGetArticleTitles_multiple_h2_titles(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append("## [Living In An Inadequate World](https://equilibriabook.com/living-in-an-inadequate-world/)")
        post_analyzer.lines.append("* Even inadequate systems only have a finite amount of failure")
        post_analyzer.lines.append("  * The true alternative is to realize that society doesn't *always* know better and then decide for yourself on a case-by-case basis")
        post_analyzer.lines.append("## [Blind Empiricism](https://equilibriabook.com/blind-empiricism/)")
        post_analyzer.lines.append("* Build theoretical frameworks, and then abandon them when reality proves them wrong")
        article_titles = post_analyzer.get_article_titles_and_urls()
        self.assertEqual(len(article_titles), 2)
        self.assertEqual(article_titles[0][0], "Living In An Inadequate World")
        self.assertEqual(article_titles[0][1], "https://equilibriabook.com/living-in-an-inadequate-world/")
        self.assertEqual(article_titles[1][0], "Blind Empiricism")
        self.assertEqual(article_titles[1][1], "https://equilibriabook.com/blind-empiricism/")

    def testGetPostDate(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append("date: 2017-04-29 18:00 -0700")
        post_date = post_analyzer.get_post_date()
        self.assertEqual(post_date.year, 2017)
        self.assertEqual(post_date.month, 4)
        self.assertEqual(post_date.day, 29)

    def testGetNotesURL(self):
        post_analyzer = self.StubbedPostAnalyzer()
        post_analyzer.lines.append("date: 2017-04-29 18:00 -0700")
        notes_url = post_analyzer.get_notes_url()
        self.assertEqual(notes_url, "https://palegreendot.net/rrg_notes/2017/04/29/rrg-reading-notes.html")

    

if __name__ == "__main__":
    unittest.main()
