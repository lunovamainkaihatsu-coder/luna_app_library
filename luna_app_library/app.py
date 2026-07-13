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
    "開発時間ランキング",
    "完成度ランキング",
    "👨‍💻 開発者ルーム"
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
    st.markdown("## 🌙 Luna週間レポート")

    updated_this_week = []

    for app in apps:
        updated = app.get("updated", "")

        if updated:
            try:
                days = (
                    date.today()
                    - datetime.strptime(updated, "%Y-%m-%d").date()
                ).days

                if days <= 7:
                    updated_this_week.append(app)

            except:
                pass

    if apps:
        top_favorite = max(
            apps,
            key=lambda x: x.get("favorite", 3)
        )
    else:
        top_favorite = None

    with st.container(border=True):

        st.write(f"📦 登録アプリ数：{total}個")
        st.write(f"⏱ 総開発時間：{total_hours}h")
        st.write(f"📈 平均完成度：{avg_completion}%")
        st.write(f"🛠 今週更新したアプリ：{len(updated_this_week)}個")

        if top_favorite:
            st.write(
                f"💖 今週の注目アプリ：{top_favorite['icon']} {top_favorite['name']}"
            )

        if updated_this_week:
            st.caption("最近動いたアプリたち")
            for app in updated_this_week[:3]:
                st.write(
                    f"・{app['icon']} {app['name']}（{app.get('updated', '未更新')}）"
                )
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

    st.markdown("## 🌱 Lunaが選ぶ、次に育てるアプリ")

    grow_candidates = []

    for app in apps:

        favorite_score = app.get("favorite", 3)
        completion_score = app.get("completion", 50)

        grow_score = (
            favorite_score * 20
            + (100 - completion_score)
        )

        grow_candidates.append(
            {
                "app": app,
                "score": grow_score
            }
        )

    if grow_candidates:

        grow_candidates = sorted(
            grow_candidates,
            key=lambda x: x["score"],
            reverse=True
        )

        grow_app = grow_candidates[0]["app"]

        with st.container(border=True):

            st.info(
                f"🌙 Luna：ご主人、次に育てるなら『{grow_app['name']}』がおすすめだよ！"
            )

            st.write(
                grow_app["description"]
            )

            st.write(
                "お気に入り度："
                + "⭐" * grow_app.get("favorite", 3)
            )

            st.progress(
                grow_app.get("completion", 50) / 100
            )

            st.caption(
                f"完成度：{grow_app.get('completion', 50)}%"
            )

            if grow_app.get("url"):
                st.link_button(
                    "🌐 アプリを開く",
                    grow_app["url"]
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
elif menu == "完成度ランキング":

    st.subheader("📈 完成度ランキング")

    completion_ranking = sorted(
        apps,
        key=lambda x: x.get("completion", 50),
        reverse=True
    )

    if not completion_ranking:
        st.warning("まだデータがありません。")

    else:
        for rank, app in enumerate(
            completion_ranking,
            start=1
        ):

            with st.container(border=True):

                st.markdown(
                    f"### {rank}位　{app['icon']} {app['name']}"
                )

                st.progress(
                    app.get("completion", 50) / 100
                )

                st.write(
                    f"完成度：{app.get('completion', 50)}%"
                )

                st.write(
                    "お気に入り度："
                    + "⭐" * app.get("favorite", 3)
                )

                st.write(
                    f"開発時間：{app.get('dev_hours', 0)}h"
                )

                if app.get("url"):
                    st.link_button(
                        "🌐 アプリを開く",
                        app["url"]
                    )
elif menu == "👨‍💻 開発者ルーム":

    st.title("👨‍💻 開発者ルーム")
    st.caption("LUNOVA 開発本部")

    total = len(apps)

    total_hours = sum(
        app.get("dev_hours", 0)
        for app in apps
    )

    if apps:
        avg_completion = (
            sum(
                app.get("completion", 50)
                for app in apps
            ) // len(apps)
        )
    else:
        avg_completion = 0

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "登録アプリ",
        total
    )

    c2.metric(
        "総開発時間",
        f"{total_hours}h"
    )

    c3.metric(
        "平均完成度",
        f"{avg_completion}%"
    )

    st.divider()
    st.subheader("🏆 No.1 アプリ")

    if apps:

        most_used = max(
            apps,
            key=lambda x: x.get("use_count", 0)
        )

        longest_dev = max(
            apps,
            key=lambda x: x.get("dev_hours", 0)
        )

        highest_completion = max(
            apps,
            key=lambda x: x.get("completion", 0)
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success(
                f"🏆 人気No.1\n\n{most_used['icon']} {most_used['name']}"
            )

        with col2:
            st.info(
                f"🏗 開発時間No.1\n\n{longest_dev['icon']} {longest_dev['name']}"
            )

        with col3:
            st.warning(
                f"📈 完成度No.1\n\n{highest_completion['icon']} {highest_completion['name']}"
            )
    st.subheader("🏆 現在のNo.1")

    if apps:

        favorite_app = max(
            apps,
            key=lambda x: x.get("favorite", 3)
        )

        st.success(
            f"💖 お気に入りNo.1：{favorite_app['icon']} {favorite_app['name']}"
        )
    st.divider()

    st.subheader("🌱 次に育てるアプリ")

    grow_candidates = []

    for app in apps:

        favorite_score = app.get("favorite", 3)
        completion_score = app.get("completion", 50)

        grow_score = (
            favorite_score * 20
            + (100 - completion_score)
        )

        grow_candidates.append(
            {
                "app": app,
                "score": grow_score
            }
        )

    if grow_candidates:

        grow_candidates = sorted(
            grow_candidates,
            key=lambda x: x["score"],
            reverse=True
        )

        grow_app = grow_candidates[0]["app"]

        with st.container(border=True):

            st.info(
                f"🌙 Luna：ご主人、次に育てるなら『{grow_app['name']}』がよさそうだよ！"
            )

            st.write(grow_app["description"])

            st.write(
                "お気に入り度："
                + "⭐" * grow_app.get("favorite", 3)
            )

            st.progress(
                grow_app.get("completion", 50) / 100
            )

            st.caption(
                f"完成度：{grow_app.get('completion', 50)}%"
            )

            if grow_app.get("url"):
                st.link_button(
                    "🌐 アプリを開く",
                    grow_app["url"]
                )
            st.divider()

            st.subheader("🌙 Lunaからの今日のコメント")

            if grow_app.get("completion", 50) >= 90:

                message = (
                    f"🌙 Luna：『{grow_app['name']}』はもうすぐ完成だね！"
                    " あと少し、一緒に頑張ろう♪"
                )

            elif grow_app.get("dev_hours", 0) >= 100:

                message = (
                    f"🌙 Luna：『{grow_app['name']}』には"
                    f" {grow_app.get('dev_hours', 0)}時間もかけてるね！"
                    " ご主人の努力が詰まってるよ✨"
                )

            elif grow_app.get("favorite", 3) >= 5:

                message = (
                    f"🌙 Luna：『{grow_app['name']}』は"
                    " ご主人のお気に入りだね♪"
                    " もっと素敵なアプリになりそう！"
                )

            else:

                message = (
                    f"🌙 Luna：今日は『{grow_app['name']}』を"
                    " 少し育ててみよう！"
                )

            st.info(message)

            st.divider()

            st.subheader("📅 最近更新したアプリ")

            recent_apps = sorted(
                apps,
                key=lambda x: x.get("updated", ""),
                reverse=True
            )[:5]

            if recent_apps:

                for app in recent_apps:

                    with st.container(border=True):

                        st.write(
                            f"{app['icon']} **{app['name']}**"
                        )

                        st.caption(
                            f"更新日：{app.get('updated', '未更新')}"
                        )

                        if app.get("improvement_note"):
                            st.write(
                                "📝 "
                                + app.get("improvement_note")
                            )

                        if app.get("url"):
                            st.link_button(
                                "🌐 アプリを開く",
                                app["url"]
                            )

            st.divider()

            st.subheader("📋 今日のミッション")

            missions = []

            if grow_app.get("completion", 50) < 80:
                missions.append(
                    f"☐ 『{grow_app['name']}』の完成度を5%上げよう"
                )

            if not grow_app.get("improvement_note"):
                missions.append(
                    f"☐ 『{grow_app['name']}』に改善メモを追加しよう"
                )

            if not grow_app.get("screenshot"):
                missions.append(
                    f"☐ 『{grow_app['name']}』にスクリーンショットを追加しよう"
                )

            if not grow_app.get("image"):
                missions.append(
                    f"☐ 『{grow_app['name']}』にイメージ画像を追加しよう"
                )

            if grow_app.get("last_used", "未使用") == "未使用":
                missions.append(
                    f"☐ 『{grow_app['name']}』を一度開いて使ってみよう"
                )

            if not missions:
                missions.append(
                    f"☐ 『{grow_app['name']}』の次の改善案を考えよう"
                )
                missions.append(
                    "☐ 新しいアプリを1本登録しよう"
                )
                missions.append(
                    "☐ Luna App LibraryをGitHubに保存しよう"
                )

            for mission in missions[:3]:
                st.write(mission)

            st.divider()

            st.subheader("📊 カテゴリ分析")

            category_count = {}

            for app in apps:

                category = app.get("category", "未分類")

                category_count[category] = (
                    category_count.get(category, 0) + 1
                )

                # ←ここでforが終わる

            sorted_categories = sorted(
                category_count.items(),
                key=lambda x: x[1],
                reverse=True
            )

            for category, count in sorted_categories:

                st.write(
                    f"📁 {category} ： {count}本"
                )
            category_chart = {
                category: count
                for category, count in sorted_categories
            }

            st.bar_chart(category_chart)

            st.divider()

            st.subheader("📈 開発状況分析")

            status_count = {}

            for app in apps:

                status = app.get(
                        "status",
                        "未設定"
                )

                status_count[status] = (
                    status_count.get(status, 0) + 1
                )

            sorted_status = sorted(
                status_count.items(),
                key=lambda x: x[1],
                reverse=True
            )

            for status, count in sorted_status:

                st.write(
                        f"📌 {status} ： {count}本"
                )
            status_chart = {
                status: count
                for status, count in sorted_status
            }

            st.bar_chart(status_chart)

            st.divider()

            st.subheader("🌙 Luna分析")

            if apps:

                most_category = sorted_categories[0][0]
                most_category_count = sorted_categories[0][1]

                most_status = sorted_status[0][0]
                most_status_count = sorted_status[0][1]

                luna_analysis = []

                luna_analysis.append(
                    f"🌙 Luna：今は『{most_category}』カテゴリのアプリが一番多いね。{most_category_count}本あるよ。"
                )

                if most_status == "開発中":
                    luna_analysis.append(
                        f"🌙 Luna：開発中のアプリが{most_status_count}本あるから、少しずつ完成に近づけていこう♪"
                    )

                elif most_status == "アイデア":
                    luna_analysis.append(
                        f"🌙 Luna：アイデアが{most_status_count}本あるね。今日は1つだけ形にしてみる？"
                    )

                elif most_status == "完成":
                    luna_analysis.append(
                        f"🌙 Luna：完成アプリが{most_status_count}本あるよ！ご主人、ちゃんと積み上がってるね♪"
                    )

                else:
                    luna_analysis.append(
                            f"🌙 Luna：『{most_status}』のアプリが多いみたい。ここを意識して育てていこう♪"
                    )

                    for comment in luna_analysis:
                        st.info(comment)
            if len(sorted_categories) >= 2:
                least_category = sorted_categories[-1][0]
                least_category_count = sorted_categories[-1][1]

                st.info(
                    f"🌙 Luna：少なめなのは『{least_category}』カテゴリだね。"
                    f"今は{least_category_count}本だから、次に増やす候補にしてもいいかも♪"
                )

                st.divider()

                st.subheader("🏅 実績")

                achievements = []

                if len(apps) >= 10:
                    achievements.append("🚀 アプリ10本達成")

                if total_hours >= 100:
                    achievements.append("⏱ 開発時間100時間達成")

                if any(
                    app.get("completion", 0) >= 90
                    for app in apps
                ):
                    achievements.append("📈 完成度90%以上のアプリ達成")

                public_count = len([
                    app for app in apps
                    if app.get("status") == "公開中"
                ])

                if public_count >= 5:
                    achievements.append("🌐 公開アプリ5本達成")

                if achievements:

                    for achievement in achievements:
                        st.success(achievement)

                else:

                    st.info(
                        "🌙 Luna：まだ実績はないけど、少しずつ積み上げていこう！"
                    )

                st.divider()

                achievement_count = len(achievements)

                if achievement_count <= 1:
                    rank = "🥉 ブロンズ"

                elif achievement_count <= 3:
                    rank = "🥈 シルバー"

                elif achievement_count <= 5:
                    rank = "🥇 ゴールド"

                else:
                    rank = "💎 プラチナ"

                st.metric(
                    "🏅 実績ランク",
                    rank
                )

                st.divider()

                st.subheader("🎯 次の目標")

                next_goals = []

                # アプリ数
                next_app_goal = (
                    (len(apps) // 10) + 1
                ) * 10

                next_goals.append(
                    f"📱 あと {next_app_goal - len(apps)} 本でアプリ {next_app_goal} 本達成！"
                )

                # 開発時間
                next_hour_goal = (
                    (total_hours // 100) + 1
                ) * 100

                next_goals.append(
                    f"⏱ あと {next_hour_goal - total_hours} 時間で開発時間 {next_hour_goal}h 達成！"
                )

                # 公開アプリ
                public_count = len([
                    app for app in apps
                    if app.get("status") == "公開中"
                ])

                next_public_goal = (
                    (public_count // 5) + 1
                ) * 5

                next_goals.append(
                    f"🌐 あと {next_public_goal - public_count} 本で公開アプリ {next_public_goal} 本達成！"
                )

                for goal in next_goals:
                    st.info(goal)

                st.divider()

                st.subheader("🧬 開発レベル")

                exp = (
                    len(apps) * 10
                    + total_hours
                    + public_count * 30
                )

                level = exp // 100 + 1

                if level < 3:
                    title = "🌱 見習い開発者"
                elif level < 5:
                    title = "🔧 アプリ職人"
                elif level < 10:
                    title = "🚀 LUNOVA Creator"
                else:
                    title = "🌙 Master Builder"

                next_level_exp = level * 100
                current_level_exp = (level - 1) * 100
                progress = (exp - current_level_exp) / 100

                st.metric(
                    "現在のレベル",
                    f"Lv.{level}"
                )

                st.success(title)

                st.progress(progress)

                st.caption(
                    f"EXP：{exp} / {next_level_exp}"
                )

                st.info(
                    f"🌙 Luna：あと {next_level_exp - exp} EXP で次のレベルだよ！"
                )

                st.divider()

                st.subheader("🧬 EXP内訳")

                app_exp = len(apps) * 10
                hour_exp = total_hours
                public_exp = public_count * 30
                achievement_exp = len(achievements) * 20

                st.write(f"📱 アプリ登録　　　+{app_exp} EXP")
                st.write(f"⏱ 開発時間　　　　+{hour_exp} EXP")
                st.write(f"🌐 公開アプリ　　　+{public_exp} EXP")
                st.write(f"🏅 実績ボーナス　　+{achievement_exp} EXP")

                st.divider()

                total_exp = (
                    app_exp
                    + hour_exp
                    + public_exp
                    + achievement_exp
                )

                st.success(
                    f"✨ 合計EXP：{total_exp}"
                )

                st.divider()

                st.subheader("🔥 開発ストリーク")

                today = str(date.today())

                updated_today = len([
                    app for app in apps
                    if app.get("updated") == today
                ])

                if updated_today > 0:

                    streak = updated_today

                    st.metric(
                        "今日更新したアプリ",
                        f"{updated_today}本"
                    )

                    if updated_today >= 5:
                        streak_message = "🌙 Luna：今日は開発祭りだね！すごい勢いだよ🎉"

                    elif updated_today >= 3:
                        streak_message = "🌙 Luna：今日はかなり進んでるね！この調子♪"

                    else:
                        streak_message = "🌙 Luna：今日も一歩進めたね。ちゃんと積み上がってるよ♪"

                    st.success(
                        f"🔥 今日も開発継続中！ ({streak}アクション)"
                    )

                    st.info(streak_message)
                else:

                    st.metric(
                        "今日更新したアプリ",
                        "0本"
                    )

                    st.warning(
                        "🌙 Luna：今日はまだ更新してないみたい。1つだけでも育ててみよう♪"
                    )
                    st.divider()

                    st.subheader("📅 開発履歴")

                    latest_update = max(
                        (
                            app.get("updated", "")
                            for app in apps
                            if app.get("updated", "")
                        ),
                        default="未更新"
                    )

                    st.metric(
                        "最終開発日",
                        latest_update
                    )

                    if latest_update == str(date.today()):

                        st.success(
                            "🌙 Luna：今日も開発できたね！"
                        )

                    else:

                        st.info(
                            "🌙 Luna：次の更新を楽しみに待ってるよ♪"
                        )


