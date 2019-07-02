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

    def get_organization_name(self):
        try:
            org_name = self.clinical_trial.responsible_party.investigator_affiliation
        except AttributeError:
            org_name = None

        if org_name is not None and org_name.text.strip() != "":
            # print(org_name.text)
            return org_name.text.strip().lower()

        # org_name = clinical_trial.responsible_party.organization
        # if (org_name != None and org_name.text.strip() != ""):
        # print(org_name.text)
        # return org_name.text.strip().lower()

        try:
            org_name = self.clinical_trial.overall_official.affiliation
        except AttributeError:
            org_name = None

        if org_name is not None and org_name.text.strip() != "":
            # print(org_name.text)
            return org_name.text.strip().lower()

        # org_name = clinical_trial.source
        # if (org_name != None and org_name.text.strip() != ""):
        # print(org_name.text)
        # return org_name.text.strip().lower()

        print(self.clinical_trial.id_info.nct_id.text, 'doesn\'t have an organization.')
        return ""

    def get_mail(self, last_name, initial):
        try:
            mail = self.clinical_trial.clinical_results.point_of_contact.email
        except AttributeError:
            mail = None

        if mail is not None:
            mail = mail.text.split(";")
            return mail[0].strip()

        try:
            mail = self.clinical_trial.location
        except AttributeError:
            mail = None

        if mail is not None:
            contacts = [contact for contact in mail.findAll() if contact.name == 'contact']
            for contact in contacts:
                if(self.extrapolate_name_parts(contact.find('last_name').text)[0] == last_name and
                        self.extrapolate_name_parts(contact.find('last_name').text)[1] == initial and
                        contact.find('email') is not None):
                    return contact.find('email').text.strip()

        return None

    def get_name(self, correct_last_name, correct_first_name_initial):
        # I get the name from the 3 possible locations
        try:
            name_1 = self.clinical_trial.overall_official.last_name
        except AttributeError:
            name_1 = None

        try:
            name_2 = self.clinical_trial.responsible_party.investigator_full_name
        except AttributeError:
            name_2 = None

        try:
            name_3 = self.clinical_trial.overall_contact.last_name
        except AttributeError:
            name_3 = None

        # I get the right name, the one that coincides with the name on the gold standard
        name = None
        if (name_1 is not None and self.extrapolate_name_parts(name_1.text)[0] == correct_last_name and
                self.extrapolate_name_parts(name_1.text)[1] == correct_first_name_initial):
            name = name_1
        if (name_2 is not None and self.extrapolate_name_parts(name_2.text)[0] == correct_last_name and
                self.extrapolate_name_parts(name_2.text)[1] == correct_first_name_initial):
            name = name_2
        if (name_3 is not None and self.extrapolate_name_parts(name_3.text)[0] == correct_last_name and
                self.extrapolate_name_parts(name_3.text)[1] == correct_first_name_initial):
            name = name_3

        return name
