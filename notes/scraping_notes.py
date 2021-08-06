entry.link.get("href") #link to filing
entry.category.get("term") # form type

date = entry.updated.text
pydate = parse(date) # using dateutil library
print(pydate.strftime("on %A, %B %d %Y at %H:%M%p"))

start_name = title.index(" - ") +3
end_name = title.index("(")
name = hard_title[start_name:end_name]

start_cik = title.index("(") +2
end_cik = hard_title.index(")")
cik = hard_title[start_cik:end_cik]