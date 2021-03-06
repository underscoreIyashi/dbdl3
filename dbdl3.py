import requests, os, pickle

def blacklist(blacklist, general):
    for b in blacklist.split():
        if b in general:
            return False
    return True

def localtag(tag, general):
    for t in tag.split():
        if t not in general:
            return False
    return True


def printsauces(datas):
    # Essentials
    print("Artist: " + datas["tag_string_artist"])
    print("ID    : " + str(datas["id"]))
    print("Pixiv : " + str(datas["pixiv_id"]))
    if "pixiv" in datas["source"]:
        source = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + source.split("/")[-1].split("_")[0].split(".")[0]
        print("Source: " + source)
    else:
        print("Source: " + datas["source"])
    print("Tags  : " + datas["tag_string"])
    print("Chars : " + datas["tag_string_character"])

def sauces(folder):
    os.chdir(folder)
    with open(folder+".dbdl", "rb") as sourcefile:
        sdic = pickle.load(sourcefile)

    print("Input the ID of the picture")
    print("eg: s_420123.png > 420123")
    print("Input something else to get bak\n")

    while 1:
        pid = input(">>> ")
        try:
            pid = int(pid)
            printsauces(sdic[pid])
        except ValueError:
            return 0
        except KeyError:
            print("Not found :(")
            pid = 0

    


def dandl(tag, local):
    """Downloading pictures from danbooru with the supplied tags
    Will return False is tag sting is empty"""  
    if len(tag) == 0:
        return False
    if os.path.exists("blacklist.txt"):
        with open("blacklist.txt", "r") as blf:
            blt = blf.read()
    else:
        blt = ""

        if os.path.exists(tag) == False:
        os.mkdir(tag)
    os.chdir(tag)
    
    page = 0
    score = 0
    skipped = 0
    sourcefile = {}
    pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&page=" + str(page)).json()
    print("Downloaded / Skipped")
    while len(pjson) > 0:
        for item in pjson:
            if blacklist(blt, item["tag_string"]) and localtag(local, item["tag_string"]) and ("file_url" in item):
                pic = requests.get("http://donmai.us" + item["file_url"]).content
                filename = item["rating"] + "_" + str(item["id"]) + "." + item["file_ext"]
                print("{}/{}: {}".format(score, skipped, filename), end="\r")
                
                with open(filename, "wb") as fpic:
                    fpic.write(pic)
                score += 1
                try:
                    sourcefile[item["id"]] = item
                    with open(tag + ".dbdl", "wb") as sf:
                        pickle.dump(sourcefile, sf)
                except:
                    pass
            else:
                skipped += 1

        page += 1
        pjson = requests.get("http://donmai.us/posts.json?tags=" + tag + "&page=" + str(page)).json()
        
    print("Downloaded {} pictures, skipped {}".format(score, skipped))
    os.chdir("..")
#    achievements(1, score)
    print("----------------------------------------")

#---------------------

print("Loading...", end="\r")
print("-*- Danbooru Downloader 3 -*-")
print("                 python ^")
print("-----------------------------")
print("* Input some tags to begin *")
print("Alternatively, input a letter", "to do something else.", sep="\n")
print("[b] Local blacklisting")
print("[s] Info and sources")
while 1:
    thing = input(">>>")
    if thing == "b":
        blt = input("Input tags: ")
        with open("blacklist.txt", "w") as blf:
            blf.write(blt)
    elif thing == "s":
        print("Enter a folder name")
        sltskyneo = input(">>> ")
        sauces(sltskyneo)
        
    else:
        local = input("Local tags:")
        dandl(thing, local)
