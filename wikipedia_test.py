import re
from create_html import wikipedia_html

reference1 = {'title': 'Kirn, Walter (11 June 2000).',
              'link_title': "\"Happy Families Are Not All Alike\"",
              'link_url': 'https://movies2.nytimes.com/books/00/06/11/reviews/000611.11kirngt.html'}

reference2 = {'title': 'Maslin, Janet (8 June 2000).',
              'link_title': "\"BOOKS OF THE TIMES; Wising Up, Though He Ain't No Bigger Than a Poot (Published 2000)\"",
              'link_url': 'https://www.nytimes.com/2000/06/08/books/books-of-the-times-wising-up-though-he-ain-t-no-bigger-than-a-poot.html'}

reference3 = {'title': 'Optics, Hecht, 4th edition, pp. 386-7'}

mother_string = """His mother's name is Elizabeth.
She has three brothers: James, John, and Johnson."""

education_string = """Jim was homeschooled until high school."""

TOC_section_1_1 = [{'title': 'Mother',
                    'number': '1.1.1',
                    'text': mother_string},
                   {'title': 'Uncles',
                    'number': '1.1.2'}]

TOC_section_1 = [{'title': 'Family',
                  'number': '1.1',
                  'children': TOC_section_1_1},
                 {'title': 'Education',
                  'number': '1.2'},
                 {'title': 'Religious formation',
                  'number': '1.3'}]



TOC_section_2 = [{'title': 'High school',
                  'number': '2.1'},
                 {'title': 'University',
                  'number': '2.2'}]

TOC = {'children': [{'title': 'Early life',
                     'number': '1',
                     'children': TOC_section_1},
                    {'title': 'Education',
                     'number': '2',
                     'children': TOC_section_2,
                     'text': education_string},
                    {'title': 'Death',
                     'number': '3'}]}

intro_string = """is a coming-of-age novel by Tony Earley, published by Little, Brown in 2000. It details the early life of Jim Glass, who lives with his mother, Elizabeth, and three uncles, in the small fictional town of Aliceville, North Carolina, also known as "Jim the Town".
It is widely regarded as the best book of all time."""

content = {'title': 'Jim the Boy',
           'url': 'Jim_the_Boy',
           'introduction': intro_string,
           'references': [reference1, reference2, reference3],
           'languages': ['Deutsch', 'עברית', '中文'],
           'categories': ['2000 American novels', 'Novels set in North Carolina', 'Little, Brown and Company books',
                          'American bildungsromans', '2000s young adult novel stubs', 'Bildungsroman stubs'],
           'TOC': TOC}


def main():
    html = wikipedia_html(content)
    html_file = open('alternet/wiki/html_TOC_test.html', "w")
    html_file.write(html)
    html_file.close()


if __name__ == "__main__":
    main()
