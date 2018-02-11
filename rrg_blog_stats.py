import dateutil.parser
import glob
import re
import os
import csv
import sys

class PostAnalyzer:
    def __init__(self, post_filename):
        file_handle = open(post_filename, 'r')
        self.filename = post_filename
        self.lines = list(file_handle)

    def get_date(self):
        """Because of limitations in Jekyll, the actual date field on each
        .markdown file corresponds to the date I posted the notes, rather than
        the meeting date. However, for the purposes of the statistics, we're
        interested in the meeting dates, so I'm parsing that out of the title.
        It's a dirty hack, but I thank past!quanticle for making said dirty
        hack possible by being consistent with the post title format."""

        date_regex = re.compile(r'^title: "(\w+ \d+ \d{4}) RRG Notes"')
        for line in self.lines:
            match = date_regex.match(line)
            if match:

                meeting_date_str = match.group(1)
                return dateutil.parser.parse(meeting_date_str)

        return None #If there is no date on the file (for some reason), what 
                    #can we do? In such a situation, returning None is better
                    #than throwing an exception, because we can just map None
                    #to empty string

    def get_article_titles_and_urls(self):
        article_title_and_url_regex = re.compile(r'^#+ \[(.*)\]\((.*)\)')
        article_titles_and_urls = []
        for line in self.lines:
            match = article_title_and_url_regex.match(line)
            if match:
                article_titles_and_urls.append((match.group(1), match.group(2)))
        return article_titles_and_urls

class RRGBlogAnalyzer:

    def __init__(self, posts_dir, output_file_name):
        self.filenames = self._get_rrg_notes_files(posts_dir)
        self.output_file_name = output_file_name

    def _get_rrg_notes_files(self, posts_dir):
        glob_str = os.path.join(posts_dir, "*rrg-reading-notes.markdown")
        return glob.glob(glob_str)

    def analyze_rrg_blog(self):
        with open(self.output_file_name, 'w', newline='') as output_csv_file:
            analysis_writer = csv.writer(output_csv_file)
            for filename in self.filenames:
                print("Analyzing {}".format(filename)) #DEBUG
                post_analyzer = PostAnalyzer(filename)
                post_datetime = post_analyzer.get_date()
                articles_and_urls = post_analyzer.get_article_titles_and_urls()
                for article_url_pair in articles_and_urls:
                    analysis_writer.writerow([str(post_datetime.date()), article_url_pair[0], article_url_pair[1]])

def print_usage_and_exit():
    print("Usage: rrg_blog_stats.py <posts_dir> <output_file_name>")
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage_and_exit()
    blog_analyzer = RRGBlogAnalyzer(sys.argv[1], sys.argv[2])
    blog_analyzer.analyze_rrg_blog()
