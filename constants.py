EXPERIENCE_FIELDS = {'Company Name', 'Dates Employed', 'Employment Duration', 'Location'}
EDUCATION_FIELDS = {'Degree Name', 'Field Of Study', "Dates attended or expected graduation"}
FIELDS = EXPERIENCE_FIELDS.union(EDUCATION_FIELDS)

LOCS = {}
XPATHS = {}
# XPATH locations for each section (loc) and its fields (xpath)
LOCS["Experience"] = '//*[@id = "experience-section"]'
LOCS["Education"] = '//*[@id = "education-section"]'
LOCS["Skills"] = '//*[@class="pv-profile-section pv-skill-categories-section artdeco-container-card ember-view"]'

XPATHS["Experience"] = ''.join([LOCS["Experience"], r"//ul//li"])
XPATHS["Education"] = ''.join([LOCS["Education"], r"//ul//li"])
XPATHS["Skills"] = ''.join([LOCS["Skills"], r"//li"])

SCROLL_PAUSE_TIME = 1
FAILED_SECTION_SCRAPE="Failed to parse section: {}.\n Got Error: {}"
DEFAULT_SECTIONS=["Experience","Education","Skills"]







if __name__=="__main__":



    print("All tests passed")