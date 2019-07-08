from pymaybe import maybe


class Article:

    def __init__(self, article):
        self.article = article

    def get_affiliation_tag(self, last_name, initial):
        authors = self.article.MedlineCitation.Article.AuthorList
        for author in authors.findAll():

            if (maybe(author).find('LastName').text.lower() == last_name and
                    maybe(author).find('Initials').text.lower()[0] == initial):
                pass
            else:
                continue

            return author.find('Affiliation')
        return None

    @staticmethod
    def extrapolate_name(name):
        if name is None:
            return None, None, None
        for child in name.findAll():
            if child.name == 'LastName':
                last_name = child.text.lower()
            if child.name == 'ForeName':
                first_name = child.text.lower()
            if child.name == 'Initials':
                first_name_initial = child.text.lower()[0]
        return last_name, first_name_initial, first_name

    # I need to find the right author because in PubMed he/she is not always the first on the list
    def get_name(self, last_name, initial):
        authors = self.article.MedlineCitation.Article.AuthorList

        for author in authors.findAll():
            if (maybe(author).find('LastName').text.lower() == last_name and
                    maybe(author).find('Initials').text.lower()[0] == initial):
                return author
        return None

    def get_organization_name(self, last_name, initial):
        affiliation = self.get_affiliation_tag(last_name, initial)

        if affiliation is not None:
            return affiliation.text.strip()

        return None

    def get_mail(self, last_name, initial):
        affiliation = self.get_affiliation_tag(last_name, initial)

        if affiliation is None:
            return None

        strings = affiliation.text.split(' ')

        mail_string = [string for string in strings if "@" in string]

        if len(mail_string) == 0:
            return None

        mail_string = mail_string[0]
        if mail_string[-1] == '.':
            mail_string = mail_string[:-1]
        return mail_string.lower().strip()

    def get_year(self):
        date = self.article.PubDate

        year = date.Year
        if year is not None:
            return year.text

        year = date.MedlineDate
        if year is not None:
            return year.text.split(' ')[0]

        return None
