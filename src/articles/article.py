from pymaybe import maybe


class Article:

    def __init__(self, article):
        self.article = article

    def get_affiliation_tag(self, last_name, initial):
        # Here I get the affiliation tag (if present) of the author with the specified last name and initial
        author = self.get_author_tag(last_name, initial)
        return author.find('Affiliation') if author is not None else None

    @staticmethod
    def extrapolate_name(name):
        # Given a tag name, I get the last name, the first name initial and the first name
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

    def get_author_tag(self, last_name, initial):
        # Here I get the tag of the author with the specified last name and initial (if the author is present)
        authors = self.article.MedlineCitation.Article.AuthorList
        for author in authors.findAll():
            if (maybe(author).find('LastName').text.lower() == last_name and
                    maybe(author).find('Initials').text.lower()[0] == initial):
                return author
        return None

    def get_organization_name(self, last_name, initial):
        # Here I get the affiliation text contained in the affiliation tag of the author
        affiliation = self.get_affiliation_tag(last_name, initial)
        if affiliation is not None:
            return affiliation.text.strip()
        return None

    def get_mail(self, last_name, initial):
        # Here I search the mail of the author in the affiliation tag (that is where it usually is in the articles)
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
        # Here I get the pubblication year of the article
        date = self.article.PubDate

        year = date.Year
        if year is not None:
            return year.text

        year = date.MedlineDate
        if year is not None:
            return year.text.split(' ')[0]

        return None

    def get_title(self):
        # I get the title of the article
        return self.article.ArticleTitle.text

    def get_text(self, mesh=False, whole_text=False):
        # I get all the text contained in the abstracts and optionally the text in the mesh terms or the whole text
        if whole_text:
            return [self.article.get_text()]
        # These are the abstracts
        texts = [abstract.text.strip() for abstract in self.article.findAll('AbstractText')]
        mesh_terms = [mesh_term.text.strip() for mesh_term in self.article.findAll('MeshHeading') if mesh]
        texts.extend(mesh_terms)
        return texts

    def get_all_texts(self):
        # Here I get title + text
        texts = self.get_text()
        texts.append(self.get_title())
        texts = " ".join(texts)
        return texts
