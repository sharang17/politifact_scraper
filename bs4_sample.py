import requests 
from bs4 import BeautifulSoup
import pandas as pd
import requests_cache




def init_cache():
    requests_cache.install_cache('bs4_test_cache', backend='sqlite', expire_after=180)

def get_job_desc(desc_url):
    page = requests.get(desc_url)
    soup_desc = BeautifulSoup(page.content,'html.parser')
    desc= soup_desc.find("div",class_="content").find_all("p")[0].text
    return desc


def get_text(column_list,col_elem_map):
    tag_list=[]
    for tag_elem,class_attr in col_elem_map.items():
        if (class_attr[0] == "a" and class_attr[1] == "card-footer-item"):
            href_link = column_list.find_all(class_attr[0],class_attr)[1].get('href')
            val = get_job_desc(href_link)
            # val = column_list.find_all(class_attr[0],class_attr)[1].get('href')
            print
        else:
            val=column_list.find(class_attr[0],class_attr[1]).text.replace(" ","").replace("\n","")
        tag_list.append({tag_elem:val})
    results = {}
    for tag in tag_list:
        results.update(tag)
    return results

    



if __name__ == '__main__':

    URL = "https://realpython.github.io/fake-jobs/"

    politifact_url = 'https://www.politifact.com/issues/'



    col_elem_map = {
        "location":("p","location"),
        "company":("h3","subtitle is-6 company"),
        "job_title":("h2","title is-5"),
        "date_posted":("p","is-small has-text-grey"),
        "href": ("a","card-footer-item")}

    card_elem  = "div"
    card_class = "card-content"
    init_cache()
    page = requests.get(URL) 

    soup = BeautifulSoup(page.content,'html.parser')

    # print(results_container.prettify())



    half_column = soup.find_all(card_elem,class_ = card_class)
    print(half_column[0].find_all("a","card-footer-item")[1].get('href'))
    half_column_dict = [get_text(hc,col_elem_map) for hc in half_column]
    df_jobs = pd.DataFrame(half_column_dict)
    # df_jobs.to_csv("check_scrape.csv")
    print(df_jobs.head())


   

    
    

    