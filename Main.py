import streamlit as st
import sqlite3
import base64
st.set_page_config(
    page_title="Simple Streamlit App",
    layout="wide",  # Use 'wide' to increase the app's width
    
)
# Database setup
def init_db():
    conn = sqlite3.connect("chapters.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chapters (
                    id INTEGER PRIMARY KEY,
                    chapter_head TEXT,
                    subheading TEXT,
                    content TEXT,
                    code TEXT,
                    image BLOB)''')
    conn.commit()
    conn.close()

init_db()

def insert_chapter(chapter_head, subheading, content, code, image):
    conn = sqlite3.connect("chapters.db")
    c = conn.cursor()
    c.execute("INSERT INTO chapters (chapter_head, subheading, content, code, image) VALUES (?, ?, ?, ?, ?)",
              (chapter_head, subheading, content, code, image))
    conn.commit()
    conn.close()

def get_all_chapters():
    conn = sqlite3.connect("chapters.db")
    c = conn.cursor()
    c.execute("SELECT * FROM chapters")
    data = c.fetchall()
    conn.close()
    return data

def update_chapter(chapter_id, chapter_head, subheading, content, code, image):
    conn = sqlite3.connect("chapters.db")
    c = conn.cursor()
    c.execute("""UPDATE chapters SET chapter_head = ?, subheading = ?, content = ?, code = ?, image = ? 
                WHERE id = ?""",
              (chapter_head, subheading, content, code, image, chapter_id))
    conn.commit()
    conn.close()

def delete_chapter(chapter_id):
    conn = sqlite3.connect("chapters.db")
    c = conn.cursor()
    c.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
    conn.commit()
    conn.close()

def image_to_bytes(image_file):
    return image_file.read() if image_file else None

# Streamlit app
def main():
    st.title("Chapter Writer")

    menu = ["Create", "View/Edit/Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create":
        st.subheader("Create a Chapter")

        with st.form("chapter_form"):
            chapter_head = st.text_input("Chapter Head")
            subheading = st.text_input("Subheading")
            content = st.text_area("Content")
            code = st.text_area("Code")
            image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
            image_bytes = image_to_bytes(image_file)

            submitted = st.form_submit_button("Submit")

            if submitted:
                insert_chapter(chapter_head, subheading, content, code, image_bytes)
                st.success("Chapter added successfully!")

    elif choice == "View/Edit/Delete":
        st.subheader("View, Edit, or Delete Chapters")

        chapters = get_all_chapters()
        for chapter in chapters:
            chapter_id, chapter_head, subheading, content, code, image = chapter

            with st.expander(f"{chapter_head} - {subheading}"):
                st.markdown(f"**Content:** {content}")
                st.markdown(f"**Code:**")
                st.code(code)
                if image:
                    st.image(base64.b64decode(image), use_column_width=True)

                edit = st.button("Edit", key=f"edit_{chapter_id}")
                delete = st.button("Delete", key=f"delete_{chapter_id}")

                if edit:
                    with st.form(f"edit_form_{chapter_id}"):
                        new_chapter_head = st.text_input("Chapter Head", value=chapter_head)
                        new_subheading = st.text_input("Subheading", value=subheading)
                        new_content = st.text_area("Content", value=content)
                        new_code = st.text_area("Code", value=code)
                        new_image_file = st.file_uploader("Upload New Image", type=["png", "jpg", "jpeg"])
                        new_image_bytes = image_to_bytes(new_image_file) or image

                        update_submitted = st.form_submit_button("Update")

                        if update_submitted:
                            update_chapter(chapter_id, new_chapter_head, new_subheading, new_content, new_code, new_image_bytes)
                            st.success("Chapter updated successfully!")

                if delete:
                    delete_chapter(chapter_id)
                    st.success("Chapter deleted successfully!")

if __name__ == "__main__":
    main()
