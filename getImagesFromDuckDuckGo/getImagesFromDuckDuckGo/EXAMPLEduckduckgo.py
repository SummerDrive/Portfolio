page.goto("https://duckduckgo.com/?t=h_&q=seascape+resort&ia=images&iax=images&iaf=size%3ALarge")
    page.get_by_role("img", name="Seascape Resort Photos").first.click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="ファイルを見る").click()
    page1 = page1_info.value
    page1.close()


def getImageURL(txtAlt,p):
    print(txtAlt)
    p.mouse.wheel(0, 2000)
    p.wait_for_timeout(2000)
    p.get_by_role("img", name=txtAlt).first.wait_for(state="visible", timeout=30000)
    p.get_by_role("img", name=txtAlt).first.click()
    print("imgOK")
    time.sleep(2)

    img_url = p.get_by_role("link", name="ファイルを見る").get_attribute("href")
    time.sleep(2)
    return img_url

def openWebsite(urlD,pw):
    #browser = pw.chromium.launch(headless=False, args=["--window-position=640,540"])
    browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context()
    page = context.new_page()
    page.goto(urlD, wait_until="domcontentloaded")
    print("gotoOK")
    time.sleep(2)
    # セーフサーチ表示部分を取得
    #safe_search = page.get_by_test_id("zci-images")

    # セーフサーチ表示を取得（標準 or 厳密 or 無効）
    safe_search = page.get_by_text("セーフサーチ：", exact=False).first
    print(type(safe_search))
    # すでに「無効（オフ）」なら何もしない
    if "無効" not in safe_search.inner_text():
        safe_search.click()                    # メニュー開く
        page.get_by_text("無効", exact=True).click()  # 「無効」を選択
    print("searchOK")
    #page.mouse.wheel(0, 2000)
    #page.wait_for_timeout(2000)
    #page.get_by_test_id("zci-images").get_by_text("無効").wait_for(state="visible", timeout=30000)
    #page.get_by_test_id("zci-images").get_by_text("無効").click()
    print("disableOK")
    time.sleep(2)

    # 特定の要素（例：`img`要素）のinnerHTMLすべてを取得
    alt_list = page.eval_on_selector_all("img", "elements => elements.map(e => e.alt)")
    trimed_list = list(set(alt_list))
    trimed_list.pop(0)
    print(trimed_list)

    array = []
    for alt in trimed_list:
        array.append(getImageURL(alt,page))
        array.append(alt)
        time.sleep(2)

    return array

        '''
        urls = [
            r["image"] for r in results
            if r["image"].lower().endswith((".jpg", ".jpeg", ".png"))
            and r.get("width", 0) >= 512
            and r.get("height", 0) >= 512
        ]

    return urls
'''