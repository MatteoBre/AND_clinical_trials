from pymaybe import maybe
from operator import attrgetter
from functools import reduce


class ClinicalTrial:

    def __init__(self, clinical_trial):
        self.clinical_trial = clinical_trial

    # Given a name, it finds the last name, initial and first name
    @staticmethod
    def extrapolate_name_parts(name):
        # I use the lower case and remove the points to uniform the later comparison
        name = name.split(',')[0].lower().replace('.',
                                                  '').strip()  # I get rid of the M.D and PhD, I only need the name now
        name = name.split(' ')
        last_name = name[-1]  # the last is always the last name (double surnames are united by '-')
        first_name = ' '.join(name[:-1])  # everythng except the last
        if first_name == '':
            return last_name
        first_name_initial = first_name[0]
        return last_name, first_name_initial, first_name

    def get_organization_name(self, last_name, initial):
        tags = self.get_all_name_tags(last_name, initial)

        for tag in tags:
            if tag.parent.investigator_affiliation is not None:
                return tag.parent.investigator_affiliation.text.strip()
            if tag.affiliation is not None:
                return tag.affiliation.text.strip()

        print(self.clinical_trial.id_info.nct_id.text, 'doesn\'t have an organization.')
        return ""

    def get_mail(self, last_name, initial):
        tags = self.get_all_name_tags(last_name, initial)

        mails = []

        points_of_contact = self.clinical_trial.findAll('point_of_contact')
        mails.extend([point.email.text.split(";")[0] for point in points_of_contact if point.email is not None])

        mails.extend([tag.email.text for tag in tags if tag.email is not None])

        for mail in mails:
            return mail.lower().strip()
        return None

    def matches(self, text, correct_last_name, correct_first_name_initial):
        parts = self.extrapolate_name_parts(text)
        return parts[0] == correct_last_name and parts[1] == correct_first_name_initial

    def get_all_name_tags(self, correct_last_name, correct_first_name_initial):
        getters = [attrgetter(a) for a in ['last_name.text'] * 2 + ['text']]
        tag_names = ['overall_contact', 'overall_official', 'investigator_full_name']
        res = [[official for official in self.clinical_trial.findAll(tag_names[i])
                if self.matches(getters[i](official), correct_last_name, correct_first_name_initial)]
               for i in range(3)]
        res = reduce(list.__add__, res)

        return res

    def get_name(self, correct_last_name, correct_first_name_initial):

        tags = self.get_all_name_tags(correct_last_name, correct_first_name_initial)

        for tag in tags:
            if tag.last_name is not None:
                return tag.last_name
            return tag
        return None

    def get_year(self):
        date = self.clinical_trial.find('study_first_submitted')

        if date is None:
            return None

        strings = date.text.split(' ')

        return strings[-1]

    def get_title(self):
        title = self.clinical_trial.brief_title
        if title is None:
            return None
        return title.text

    def get_country_and_city(self):
        locations = self.clinical_trial.findAll('location')
        countries = [location.country.text for location in locations]
        cities = [location.city.text for location in locations]
        return countries, cities

    def get_text(self, elig=False, whole_text=False):
        if whole_text:
            return [self.clinical_trial.get_text()]
        brief_summary = maybe(self).clinical_trial.brief_summary.textblock.text.strip()
        detailed_description = maybe(self).clinical_trial.detailed_description.textblock.text.strip()
        eligibility_criteria = maybe(self).clinical_trial.eligibility.criteria.textblock.text.strip() if elig else None

        arr = [str(brief_summary), str(detailed_description), str(eligibility_criteria)]
        arr = [string for string in arr if string != 'None']
        return arr

    def get_all_texts(self):
        texts = self.get_text()
        texts.append(self.get_title())
        texts = " ".join(texts)
        return texts
