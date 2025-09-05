import re
def norm_basic(s): return re.sub(r"\s+"," ",s.strip())
def norm_yesno(s): return s.strip().upper()
def norm_number_tail(s): return re.sub(r"[.,!?;:]+$","",s.strip())
def equal(a,b,mode="strict"):
    if mode=="strict": return a==b
    if mode=="spaces": return norm_basic(a)==norm_basic(b)
    if mode=="yesno":  return norm_yesno(a)==norm_yesno(b)
    if mode=="punct":  return norm_number_tail(a)==norm_number_tail(b)
    return a==b
