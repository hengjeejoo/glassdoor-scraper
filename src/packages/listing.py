# Import necessary libraries
# standard libraries
from time import time
# custom functions
try:
    from packages.common import requestAndParse
except ModuleNotFoundError:
    from common import requestAndParse


# extracts desired data from listing banner
def extract_listingBanner(listing_soup):
    listing_bannerGroup_valid = False

    try:
        listing_bannerGroup = listing_soup.find("div", class_="css-ur1szg e11nt52q0")
        listing_bannerGroup_valid = True
    except:
        print("[ERROR] Error occurred in function extract_listingBanner")
        companyName = "NA"
        company_starRating = "NA"
        company_offeredRole = "NA"
        company_roleLocation = "NA"
        company_salary = "NA"
    
    if listing_bannerGroup_valid:
        try:
            company_starRating = listing_bannerGroup.find("span", class_="css-1pmc6te e11nt52q4").getText()
        except:
            company_starRating = "NA"
        if company_starRating != "NA":
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText().replace(company_starRating,'')
                #companyName = listing_bannerGroup.find("div", class_="css-87uc0g e1tk4kwz1").getText().replace(company_starRating,'')
            except:
                companyName = "NA"
            # company_starRating.replace("★", "")
            company_starRating = company_starRating[:-1]
        else:
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText()
                #companyName = listing_bannerGroup.find("div", class_="css-87uc0g e1tk4kwz1").getText()
            except:
                companyName = "NA"

        try:
            company_offeredRole = listing_bannerGroup.find("div", class_="css-17x2pwl e11nt52q6").getText()
        except:
            company_offeredRole = "NA"

        try:
            company_roleLocation = listing_bannerGroup.find("div", class_="css-1v5elnn e11nt52q2").getText()
        except:
            company_roleLocation = "NA"
        try:
            company_salary = listing_bannerGroup.find_all("div", class_="css-1v5elnn e11nt52q2")[1].getText()
            # TODO: extract salary range. The format now is either "Employer Est.:$7K - $8K" or "$7K - $8K (Glassdoor est.)"
            # the desired format is "$7000 - $8000"
            if "Employer Est.:" in company_salary:
                company_salary = company_salary.replace("Employer Est.:", "")
            elif "(Glassdoor est.)" in company_salary:
                company_salary = company_salary.replace("(Glassdoor est.)", "")
            elif "(Glassdoor Est.)" in company_salary:
                company_salary = company_salary.replace("(Glassdoor Est.)", "")
            company_salary = company_salary.replace("$", "")
            company_salary = company_salary.replace("K", "000")
            company_salary = company_salary.replace(" ", "")
            company_salary = company_salary.replace("-", " - ")
        except Exception as e:
            #print(e)
            company_salary = "NA"

    print(companyName, company_starRating, company_offeredRole, company_roleLocation, company_salary)
    return companyName, company_starRating, company_offeredRole, company_roleLocation, company_salary


# extracts desired data from listing description
def extract_listingDesc(listing_soup):
    extract_listingDesc_tmpList = []
    listing_jobDesc_raw = None

    try:
        listing_jobDesc_raw = listing_soup.find("div", id="JobDescriptionContainer")
        if type(listing_jobDesc_raw) != type(None):
            JobDescriptionContainer_found = True
        else:
            JobDescriptionContainer_found = False
            listing_jobDesc = "NA"
    except Exception as e:
        print("[ERROR] {} in extract_listingDesc".format(e))
        JobDescriptionContainer_found = False
        listing_jobDesc = "NA"

    if JobDescriptionContainer_found:
        jobDesc_items = listing_jobDesc_raw.findAll('li')
        for jobDesc_item in jobDesc_items:
            extract_listingDesc_tmpList.append(jobDesc_item.text)

        listing_jobDesc = " ".join(extract_listingDesc_tmpList)

        if len(listing_jobDesc) <= 10:
            listing_jobDesc = listing_jobDesc_raw.getText()
    #print(listing_jobDesc)
    return listing_jobDesc


# extract data from listing
def extract_listing(url):
    #print(url)
    request_success = False
    try:
        listing_soup, requested_url = requestAndParse(url)
        request_success = True
    except Exception as e:
        print("[ERROR] Error occurred in extract_listing, requested url: {} is unavailable.".format(url))
        return ("NA", "NA", "NA", "NA", "NA", "NA", "NA")

    if request_success:
        companyName, company_starRating, company_offeredRole, company_roleLocation, company_salary = extract_listingBanner(listing_soup)
        listing_jobDesc = extract_listingDesc(listing_soup)

        return (companyName, company_starRating, company_offeredRole, company_roleLocation, company_salary, listing_jobDesc, requested_url)


if __name__ == "__main__":
    
    url = "https://www.glassdoor.sg/Job/singapore-software-developer-jobs-SRCH_IL.0,9_IC3235921_KO10,28.htm"
    start_time = time()
    returned_tuple = extract_listing(url)
    time_taken = time() - start_time
    print(returned_tuple)
    print("[INFO] returned in {} seconds".format(time_taken))