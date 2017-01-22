from django import template  
register = template.Library()

def ngminions(ngstr):
    ngstr2 = ngstr[2:].split(" or ")
    #ngstr2 = ngstr2.sort()
    return ngstr2
    
register.filter(ngminions)

def jobid_replace(jobid):
    jobid2 = jobid.replace("-","")
    return jobid2

register.filter(jobid_replace)

def txt_cut(filename):
    filename2 = filename[:-4]
    return filename2
    
register.filter(txt_cut)
