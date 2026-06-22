import streamlit as st
import json
from pathlib import Path
from datetime import date, datetime
import random

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
APP_FILE = DATA_DIR / "apps.json"

st.set_page_config(
    page_title="Luna App Library",
    page_icon="🌙",
    layout="wide"
)

def load_apps():
    if APP_FILE.exists():
        with open(APP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_apps(apps):
    with open(APP_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)

apps = load_apps()

# =====================
# 管理者ログイン
# =====================
ADMIN_PASSWORD = "lunova2026"

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

with st.sidebar.expander("🔐 管理者ログイン"):
    password = st.text_input(
        "パスワード",
        type="password"
    )

    if st.button("ログイン"):
        if password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.success("管理者としてログインしました")
        else:
            st.error("パスワードが違います")

    if st.session_state.is_admin:
        if st.button("ログアウト"):
            st.session_state.is_admin = False
            st.rerun()

for app in apps:
    app.setdefault("url", "")
    app.setdefault("use_count", 0)
    app.setdefault("last_used", "未使用")
    app.setdefault("favorite", 3)
    app.setdefault("improvement_note", "")
    app.setdefault("updated", "未更新")
    app.setdefault("completion", 50)
    app.setdefault("web_version", True)
    app.setdefault("app_version", False)
    app.setdefault("screenshot", "")
    app.setdefault("image", "")
    app.setdefault("dev_hours", 0)    
    
st.title("🌙 Luna App Library")
st.caption("ご主人が作ったアプリたちを集める母艦")

menu_items = [
    "ホーム",
    "アプリ図鑑",
    "人気ランキング",
    "開発時間ランキング"
]

if st.session_state.is_admin:
    menu_items += [
        "アプリ登録",
        "アプリ編集"
    ]

menu = st.sidebar.radio(
    "メニュー",
    menu_items
)
if menu == "ホーム":

    st.subheader("🚀 母艦ダッシュボード")

    total = len(apps)
    released = len([a for a in apps if a["status"] == "公開中"])
    developing = len([a for a in apps if a["status"] == "開発中"])
    idea = len([a for a in apps if a["status"] == "アイデア"])

    if apps:
        avg_completion = sum(
            app.get("completion", 50)
            for app in apps
        ) // len(apps)
    else:
        avg_completion = 0

    total_hours = sum(
        app.get("dev_hours", 0)
        for app in apps
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("登録アプリ", total)
    c2.metric("公開中", released)
    c3.metric("開発中", developing)
    c4.metric("アイデア", idea)
    c5.metric("平均完成度", f"{avg_completion}%")
    c6.metric("総開発時間", f"{total_hours}h")
    

    st.progress(avg_completion / 100)

    st.info("🌙 Luna：ここはご主人のアプリたちが集まる母艦だよ。")
    st.markdown("## 🆕 最近更新したアプリ")

    recent_apps = sorted(
        apps,
        key=lambda x: x.get("updated", ""),
        reverse=True
    )[:3]

    if not recent_apps:
        st.caption("まだ更新されたアプリはありません。")
    else:
        for app in recent_apps:
            with st.container(border=True):
                st.markdown(f"### {app['icon']} {app['name']}")
                st.caption("更新日：" + app.get("updated", "未更新"))

                if app.get("improvement_note"):
                    st.write(app.get("improvement_note"))

                if app.get("url"):
                    st.link_button("🌐 アプリを開く", app["url"])
    st.markdown("## ⭐ お気に入りアプリ")

    favorite_apps = sorted(
        apps,
        key=lambda x: x.get("favorite", 3),
        reverse=True
    )[:3]

    if not favorite_apps:
        st.caption("まだお気に入りアプリはありません。")
    else:
        for app in favorite_apps:
            with st.container(border=True):
                st.markdown(f"### {app['icon']} {app['name']}")
                st.write("お気に入り度：" + "⭐" * app.get("favorite", 3))
                st.caption("更新日：" + app.get("updated", "未更新"))

                if app.get("url"):
                    st.link_button("🌐 アプリを開く", app["url"])

    st.markdown("## 🚧 開発中アプリ")

    developing_apps = [
        app for app in apps
        if app.get("status") == "開発中"
    ]

    if not developing_apps:
        st.caption("現在、開発中のアプリはありません。")
    else:
        for app in developing_apps[:5]:
            with st.container(border=True):
                st.markdown(f"### {app['icon']} {app['name']}")
                st.write(app["description"])
                st.write("お気に入り度：" + "⭐" * app.get("favorite", 3))
                st.caption("更新日：" + app.get("updated", "未更新"))

                if app.get("improvement_note"):
                    st.info(
                        "📝 最新改善メモ\n\n"
                        + app.get("improvement_note", "")
                    )

                if app.get("url"):
                    st.link_button("🌐 アプリを開く", app["url"])
    st.markdown("## 🏆 人気アプリ TOP3")

    top_apps = sorted(
        apps,
        key=lambda x: x.get("use_count", 0),
        reverse=True
    )[:3]

    if top_apps:

        for rank, app in enumerate(
            top_apps,
            start=1
        ):

            st.write(
                f"{rank}位 🏅 {app['name']} "
                f"({app.get('use_count',0)}回)"
            )
    st.markdown("## 🎲 今日のおすすめ")

    if apps:

        app = random.choice(apps)

        with st.container(border=True):

            st.markdown(
                f"### {app['icon']} {app['name']}"
            )

            st.write(app["description"])

            if app.get("url"):
                st.link_button(
                    "🌐 アプリを開く",
                    app["url"]
                )
st.markdown("## 🌙 Lunaからのおすすめ")

if apps:

    unused_apps = [
        app for app in apps
        if app.get("last_used", "未使用") == "未使用"
    ]

    favorite_apps = [
        app for app in apps
        if app.get("favorite", 3) >= 4
    ]

    stale_apps = []

    for app in apps:

        updated = app.get("updated", "")

        if updated:

            try:

                days = (
                    date.today()
                    - datetime.strptime(
                        updated,
                        "%Y-%m-%d"
                    ).date()
                ).days

                if days >= 7:
                    stale_apps.append(app)

            except:
                pass

    if unused_apps:
        recommended = random.choice(unused_apps)

        luna_messages = [
            f"🌙 Luna：ご主人、『{recommended['name']}』はまだ使ってないみたいだよ？",
            f"🌙 Luna：このアプリ、まだ眠ってるみたい。起こしてみない？",
            f"🌙 Luna：未使用のアプリを見つけたよ。今日はこれを試してみよう♪"
        ]

    elif stale_apps:
        recommended = random.choice(stale_apps)

        luna_messages = [
            f"🌙 Luna：ご主人、『{recommended['name']}』は最近更新してないみたいだよ？",
            f"🌙 Luna：このアプリ、そろそろ育ててあげない？",
            f"🌙 Luna：しばらく触ってないみたいだから気になっちゃった♪"
        ]

    elif favorite_apps:
        recommended = random.choice(favorite_apps)

        luna_messages = [
            f"🌙 Luna：ご主人のお気に入り、『{recommended['name']}』を見てみない？",
            f"🌙 Luna：アタイ、このアプリ好きだな♪",
            f"🌙 Luna：このアプリ、もっと育てたら面白くなりそう！"
        ]

    else:
        recommended = random.choice(apps)

        luna_messages = [
            f"🌙 Luna：今日は『{recommended['name']}』を見てみない？",
            f"🌙 Luna：今日はこのアプリが呼んでる気がする！",
            f"🌙 Luna：ご主人、これを開いてみよう♪"
        ]

    st.info(
        random.choice(luna_messages)
    )
    

    luna_messages = [
        f"🌙 Luna：ご主人、『{recommended['name']}』はお気に入りのアプリだよね♪",
        f"🌙 Luna：今日は『{recommended['name']}』を育ててみない？",
        f"🌙 Luna：アタイ、このアプリ好きだな♪",
        f"🌙 Luna：ご主人の力作を見に行こう！",
        f"🌙 Luna：今日はこのアプリが呼んでる気がする！"
    ]


    st.write(
        recommended["description"]
    )

    if recommended.get("url"):
        st.link_button(
            "🌐 アプリを開く",
            recommended["url"]
        )
elif menu == "アプリ図鑑":

    st.subheader("📚 アプリ図鑑")

    if not apps:
        st.warning("まだアプリが登録されていません。")

    else:
        search_word = st.text_input(
            "🔍 アプリ検索",
            placeholder="アプリ名・説明・カテゴリで検索"
        )

        category = st.selectbox(
            "カテゴリで絞り込み",
            ["すべて"] + sorted(list(set(a["category"] for a in apps)))
        )

        status = st.selectbox(
            "状態で絞り込み",
            ["すべて", "公開中", "開発中", "完成", "アイデア"]
        )

        sort_type = st.selectbox(
            "並び替え",
            [
                "登録順",
                "新着順",
                "完成度順",
                "お気に入り度順",
                "使用回数順",
                "最近使った順",
                "名前順"
            ]
        )

        filtered = apps

        if search_word:
            filtered = [
                a for a in filtered
                if search_word.lower() in a["name"].lower()
                or search_word.lower() in a["description"].lower()
                or search_word.lower() in a["category"].lower()
                or search_word.lower() in a.get("improvement_note", "").lower()
            ]

        if category != "すべて":
            filtered = [
                a for a in filtered
                if a["category"] == category
            ]

        if status != "すべて":
            filtered = [
                a for a in filtered
                if a["status"] == status
            ]

        if sort_type == "新着順":
            filtered = sorted(
                filtered,
                key=lambda x: x.get("updated", ""),
                reverse=True
            )

        elif sort_type == "完成度順":
            filtered = sorted(
                filtered,
                key=lambda x: x.get(
                    "completion",
                    50
                ),
                reverse=True
            )

        elif sort_type == "お気に入り度順":
            filtered = sorted(
                filtered,
                key=lambda x: x.get("favorite", 3),
                reverse=True
            )

        elif sort_type == "使用回数順":
            filtered = sorted(
                filtered,
                key=lambda x: x.get("use_count", 0),
                reverse=True
            )

        elif sort_type == "最近使った順":
            filtered = sorted(
                filtered,
                key=lambda x: x.get("last_used", "未使用"),
                reverse=True
            )

        elif sort_type == "名前順":
            filtered = sorted(
                filtered,
                key=lambda x: x.get("name", "")
            )

        st.caption(f"表示件数：{len(filtered)}件")

        for i, app in enumerate(filtered):

            with st.container(border=True):

                st.markdown(f"### {app['icon']} {app['name']}")
                st.write(app["description"])

                st.write("お気に入り度：" + "⭐" * app.get("favorite", 3))

                st.progress(app.get("completion", 50) / 100)
                st.caption(f"完成度：{app.get('completion', 50)}%")

                version_text = []

                if app.get("web_version", True):
                    version_text.append("🌐 Web版")

                if app.get("app_version", False):
                    version_text.append("📱 アプリ版")

                if version_text:
                    st.write("対応：" + " / ".join(version_text))
                else:
                    st.caption("対応：未設定")

                if app.get("improvement_note"):
                    st.info("📝 最新改善メモ\n\n" + app.get("improvement_note", ""))
                else:
                    st.caption("📝 最新改善メモ：未登録")


                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "カテゴリ",
                    app["category"]
                )

                c2.metric(
                    "状態",
                    app["status"]
                )

                c3.metric(
                    "使用回数",
                    f"{app.get('use_count', 0)} 回"
                )

                c4.metric(
                    "更新日",
                    app.get("updated", "未更新")
                )
                st.caption(f"最終使用日：{app.get('last_used', '未使用')}")
                img_col1, img_col2 = st.columns(2)

                with img_col1:

                    if app.get("screenshot"):

                        st.markdown("#### 📸 スクリーンショット")

                        try:
                            st.image(
                                app["screenshot"],
                                width=300
                            )
                        except:
                            st.caption("画像を表示できません")

                with img_col2:

                    if app.get("image"):

                        st.markdown("#### 🎨 イメージ画像")

                        try:
                            st.image(
                                app["image"],
                                width=250
                            )
                        except:
                            st.caption("画像を表示できません")

                col1, col2 = st.columns(2)
                with col1:
                    if app.get("url"):
                        st.link_button("🌐 アプリを開く", app["url"])
                    else:
                        st.caption("URL未登録")

                with col2:
                    if st.button("✅ このアプリを使った", key=f"use_{i}_{app['name']}"):
                        app["use_count"] += 1
                        app["last_used"] = str(date.today())
                        save_apps(apps)
                        st.rerun()

elif menu == "アプリ登録":

    st.subheader("➕ アプリ登録")

    with st.form("add_app"):

        name = st.text_input("アプリ名")
        icon = st.text_input("アイコン", value="📱")

        category = st.selectbox(
            "カテゴリ",
            ["AI", "占い", "読書", "習慣", "健康", "ゲーム", "学習", "生活", "その他"]
        )

        status = st.selectbox(
            "状態",
            ["公開中", "開発中", "完成", "アイデア"]
        )

        app_url = st.text_input("アプリURL", placeholder="https://...")

        favorite = st.slider(
            "お気に入り度",
            1,
            5,
            3
        )

        completion = st.slider(
            "完成度",
            0,
            100,
            50
        )
        dev_hours = st.number_input(
            "開発時間（時間）",
            min_value=0,
            value=0,
            step=1
        )
        web_version = st.checkbox(
            "Web版あり",
            value=True
        )

        app_version = st.checkbox(
            "アプリ版あり",
            value=False
        )

        improvement_note = st.text_area("最新改善メモ")
        screenshot = st.text_input(
            "スクショ画像パス"
        )

        image = st.text_input(
            "イメージ画像パス"
        )
        description = st.text_area("説明")
        
        submitted = st.form_submit_button("登録する")

        if submitted:
            if not name:
                st.error("アプリ名を入力してね。")
            else:
                new_app = {
                    "name": name,
                    "icon": icon,
                    "category": category,
                    "status": status,
                    "url": app_url,
                    "favorite": favorite,
                    "completion": completion,
                    "dev_hours": dev_hours,
                    "web_version": web_version,
                    "app_version": app_version,
                    "screenshot": screenshot,
                    "image": image,
                    "description": description,
                    "improvement_note": improvement_note,
                    "updated": str(date.today()),
                    "use_count": 0,
                    "last_used": "未使用"
                }
                apps.append(new_app)
                save_apps(apps)
                st.success("アプリを登録しました！")

elif menu == "アプリ編集":

    st.subheader("✏️ アプリ編集")

    if not apps:
        st.warning("アプリがありません")

    else:
        names = [app["name"] for app in apps]

        selected_name = st.selectbox(
            "編集するアプリ",
            names
        )

        app_index = next(
            i for i, a in enumerate(apps)
            if a["name"] == selected_name
        )

        app = apps[app_index]

        with st.form("edit_app"):

            name = st.text_input("アプリ名", value=app["name"])
            icon = st.text_input("アイコン", value=app["icon"])
            category = st.text_input("カテゴリ", value=app["category"])

            status_list = ["公開中", "開発中", "完成", "アイデア"]

            status = st.selectbox(
                "状態",
                status_list,
                index=status_list.index(app["status"])
                if app["status"] in status_list
                else 0
            )

            url = st.text_input("URL", value=app.get("url", ""))

            favorite = st.slider(
                "お気に入り度",
                1,
                5,
                app.get("favorite", 3)
            )

            completion = st.slider(
                "完成度",
                0,
                100,
                app.get("completion", 50)
            )
            dev_hours = st.number_input(
                "開発時間（時間）",
                min_value=0,
                value=app.get("dev_hours", 0),
                step=1
            )

            web_version = st.checkbox(
                "Web版あり",
                value=app.get("web_version", True)
            )

            app_version = st.checkbox(
                "アプリ版あり",
                value=app.get("app_version", False)
            )

            improvement_note = st.text_area(
                "最新改善メモ",
                value=app.get("improvement_note", "")
            )

            screenshot = st.text_input(
                "スクショ画像パス",
                value=app.get("screenshot", "")
            )

            image = st.text_input(
                "イメージ画像パス",
                value=app.get("image", "")
            )
            description = st.text_area(
                "説明",
                value=app["description"]
            )

            save_btn = st.form_submit_button("保存")

            if save_btn:
                apps[app_index]["name"] = name
                apps[app_index]["icon"] = icon
                apps[app_index]["category"] = category
                apps[app_index]["status"] = status
                apps[app_index]["url"] = url
                apps[app_index]["favorite"] = favorite
                apps[app_index]["completion"] = completion
                apps[app_index]["dev_hours"] = dev_hours
                apps[app_index]["web_version"] = web_version
                apps[app_index]["app_version"] = app_version
                apps[app_index]["improvement_note"] = improvement_note
                apps[app_index]["screenshot"] = screenshot
                apps[app_index]["image"] = image
                apps[app_index]["description"] = description
                apps[app_index]["updated"] = str(date.today())

                save_apps(apps)
                st.success("保存しました！")

        st.divider()

        st.warning("この操作は取り消せません。")

        delete_check = st.checkbox(
            "このアプリを削除する"
        )

        if delete_check:
            if st.button("🗑 アプリを削除する"):
                deleted_name = apps[app_index]["name"]

                apps.pop(app_index)
                save_apps(apps)

                st.success(
                    f"{deleted_name} を削除しました。"
                )

                st.rerun()
elif menu == "人気ランキング":

    st.subheader("🏆 人気ランキング")

    ranking = sorted(
        apps,
        key=lambda x: x.get("use_count", 0),
        reverse=True
    )

    if not ranking:
        st.warning("まだデータがありません。")

    else:
        for rank, app in enumerate(ranking, start=1):

            with st.container(border=True):

                st.markdown(f"### {rank}位　{app['icon']} {app['name']}")
                st.write(f"使用回数：{app.get('use_count', 0)} 回")
                st.write("お気に入り度：" + "⭐" * app.get("favorite", 3))
                st.caption("更新日：" + app.get("updated", "未更新"))

                if app.get("improvement_note"):
                    st.info("📝 最新改善メモ\n\n" + app.get("improvement_note", ""))

                if app.get("url"):
                    st.link_button("🌐 アプリを開く", app["url"])
elif menu == "開発時間ランキング":

    st.subheader("🏗 開発時間ランキング")

    dev_ranking = sorted(
        apps,
        key=lambda x: x.get("dev_hours", 0),
        reverse=True
    )

    if not dev_ranking:
        st.warning("まだデータがありません。")

    else:
        for rank, app in enumerate(dev_ranking, start=1):

            with st.container(border=True):

                st.markdown(
                    f"### {rank}位　{app['icon']} {app['name']}"
                )

                st.write(
                    f"開発時間：{app.get('dev_hours', 0)}h"
                )

                st.write(
                    "お気に入り度：" + "⭐" * app.get("favorite", 3)
                )

                st.progress(
                    app.get("completion", 50) / 100
                )

                st.caption(
                    f"完成度：{app.get('completion', 50)}%"
                )

                if app.get("url"):
                    st.link_button(
                        "🌐 アプリを開く",
                        app["url"]
                    )
