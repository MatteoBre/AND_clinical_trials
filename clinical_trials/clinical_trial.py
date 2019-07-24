from common_functions import common_functions
from pymaybe import maybe


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
                return tag.parent.investigator_affiliation.text
            if tag.affiliation is not None:
                return tag.affiliation.text


        '''
        try:
            org_name = self.clinical_trial.responsible_party.investigator_affiliation
        except AttributeError:
            org_name = None

        if org_name is not None and org_name.text.strip() != "":
            return org_name.text.strip()

        try:
            org_name = self.clinical_trial.overall_official.affiliation
        except AttributeError:
            org_name = None

        if org_name is not None and org_name.text.strip() != "":
            return org_name.text.strip()

        print(self.clinical_trial.id_info.nct_id.text, 'doesn\'t have an organization.')
        '''
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

    def get_all_name_tags(self, correct_last_name, correct_first_name_initial):
        tags = []

        overall_contacts = self.clinical_trial.findAll('overall_contact')
        tags.extend([official for official in overall_contacts if
                     self.extrapolate_name_parts(official.last_name.text)[0] == correct_last_name and
                     self.extrapolate_name_parts(official.last_name.text)[1] == correct_first_name_initial])

        overall_officials = self.clinical_trial.findAll('overall_official')
        tags.extend([official for official in overall_officials if
                     self.extrapolate_name_parts(official.last_name.text)[0] == correct_last_name and
                     self.extrapolate_name_parts(official.last_name.text)[1] == correct_first_name_initial])

        investigator_full_name = self.clinical_trial.findAll('investigator_full_name')
        tags.extend([official for official in investigator_full_name if
                     self.extrapolate_name_parts(official.text)[0] == correct_last_name and
                     self.extrapolate_name_parts(official.text)[1] == correct_first_name_initial])
        return tags

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

    def get_text(self):
        brief_summary = maybe(self).clinical_trial.brief_summary.textblock.text
        detailed_description = maybe(self).clinical_trial.detailed_description.textblock.text
        eligibility_criteria = maybe(self).clinical_trial.eligibility.criteria.textblock.text

        arr = [str(brief_summary), str(detailed_description), str(eligibility_criteria)]
        arr = [string for string in arr if string != 'None']
        return arr

    def get_country_and_city(self):
        locations = self.clinical_trial.findAll('location')
        countries = [location.country.text for location in locations]
        cities = [location.city.text for location in locations]
        return countries, cities
