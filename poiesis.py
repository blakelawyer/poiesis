# Poiesis: A statis site generator for blakelawyer.dev.

import os
import shutil
import markdown
import yaml
import re
from datetime import datetime
import create_artwork

navigation_bar = (
    f"<nav>\n"
    f"\t<ul>\n"
    f"\t\t<li><span class=\"site-name\">blake's cybernetic canopy</span></li>\n"
    f"\t\t<li><a href=\"index.html\" class=\"nav-home\">home</a></li>\n"
    f"\t\t<li><a href=\"html/projects.html\" class=\"nav-projects\">projects</a></li>\n"
    f"\t\t<li><a href=\"html/bookshelf.html\" class=\"nav-bookshelf\">bookshelf</a></li>\n"
    f"\t\t<li><a href=\"html/media.html\" class=\"nav-media\">media</a></li>\n"
    f"\t\t<li><a href=\"https://github.com/blakelawyer\" target=\"_blank\" class=\"nav-github\">\n"
    f"\t\t\t<i class=\"fab fa-github\"></i>\n"
    f"\t\t</a></li>\n"
    f"\t\t<li><a href=\"https://www.linkedin.com/in/blake-lawyer-949326222\" target=\"_blank\" class=\"nav-linkedin\">\n"
    f"\t\t\t<i class=\"fab fa-linkedin\"></i>\n"
    f"\t\t</a></li>\n"
    f"\t</ul>\n"
    f"</nav>\n"
)

head = (
    f"\t<meta charset=\"UTF-8\">\n"
    f"\t<meta name=\"viewport\" content=\"width=980\">\n"
    f"\t<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n"
    f"\t<title>Blake's Cybernetic Canopy</title>\n"
    f"\t<link href=\"https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap\" rel=\"stylesheet\">\n"
    f"\t<link href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css\" rel=\"stylesheet\">\n"
    f"\t<link rel=\"stylesheet\" href=\"styles.css\">\n"
)

def main():
    
    website_base_dir = "../blakelawyer.dev"

    create_site_directory(website_base_dir)
    create_artwork.pixelate()
    generate_index()
    generate_projects(website_base_dir)
    generate_bookshelf(website_base_dir)
    generate_media(website_base_dir)

def parse_markdown_with_metadata(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    metadata_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if metadata_match:
        front_matter = metadata_match.group(1)
        markdown_body = metadata_match.group(2)
        metadata = yaml.safe_load(front_matter)
    else:
        metadata = {}
        markdown_body = content

    return metadata, markdown_body

def generate_index():
    
    update_html(
        "site/index.html",
        "<!-- navigation_bar_start -->",
        "<!-- navigation_bar_end -->",
        navigation_bar,
    )
    
    update_html(
        "site/index.html",
        "<!-- head_start -->",
        "<!-- head_end -->",
        head,
    )
    
def generate_projects(website_base_dir):

    project_head = head.replace("styles.css", "../styles.css")
    project_navigation_bar = navigation_bar.replace("blake's cybernetic canopy", "blake's projects")
    project_navigation_bar = project_navigation_bar.replace("index.html", "../index.html")
    project_navigation_bar = project_navigation_bar.replace("html/projects.html", "projects.html")
    project_navigation_bar = project_navigation_bar.replace("html/bookshelf.html", "bookshelf.html")
    project_navigation_bar = project_navigation_bar.replace("html/media.html", "media.html")

    files = os.listdir("../blakelawyer.dev/docs/projects")
    files.remove("template.md")

    projects = []
    for file in files:
        metadata, _ = parse_markdown_with_metadata(f"{website_base_dir}/docs/projects/{file}")
        metadata['file'] = file.split(".")[0] + ".png"
        projects.append(metadata)

    # Sort by date, most recent first
    projects = sorted(
        projects,
        key=lambda x: x['date'],
        reverse=True
    )

    projects_content = ""
    projects_content += "\t\t\t<ul>\n"
    for project in projects:
        project_html = (
            f"\t\t\t\t<li>"
            f"<img src=\"../images/project_art/{project['file']}\">"
            f"<div class=\"text-container\">"
            f"<span class=\"title\">{project['title']}</span> "
            f"<span class=\"author\">{project['description']}</span>"
            f"</div>"
            f"</li>\n"
        )
        projects_content += project_html
    projects_content += "\t\t\t</ul>\n"

    update_html(
        "site/html/projects.html",
        "<!-- projects_start -->",
        "<!-- projects_end -->",
        projects_content,
    )

    update_html(
        "site/html/projects.html",
        "<!-- navigation_bar_start -->",
        "<!-- navigation_bar_end -->",
        project_navigation_bar,
    )

    update_html(
        "site/html/projects.html",
        "<!-- head_start -->",
        "<!-- head_end -->",
        project_head,
    )

def generate_media(website_base_dir):

    media_head = head.replace("styles.css", "../styles.css")
    media_navigation_bar = navigation_bar.replace("blake's cybernetic canopy", "blake's consumption")
    media_navigation_bar = media_navigation_bar.replace("index.html", "../index.html")
    media_navigation_bar = media_navigation_bar.replace("html/projects.html", "projects.html")
    media_navigation_bar = media_navigation_bar.replace("html/bookshelf.html", "bookshelf.html")
    media_navigation_bar = media_navigation_bar.replace("html/media.html", "media.html")
    
    files = os.listdir("../blakelawyer.dev/docs/media")
    files.remove("template.md")

    media_items = []
    for file in files:
        metadata, _ = parse_markdown_with_metadata(f"{website_base_dir}/docs/media/{file}")
        metadata['file'] = file.split(".")[0] + ".jpg"
        media_items.append(metadata)

    currently_watching = []
    completed_media = []
    for item in media_items:
        if item['completed']:
            completed_media.append(item)
        else:
            currently_watching.append(item)

    completed_media = sorted(
        completed_media,
        key=lambda x: x['date'],
        reverse=True
    )

    currently_watching_content = ""
    currently_watching_content += "\t\t\t<ul>\n"
    for item in currently_watching:
        media_html = (
            f"\t\t\t\t<li>"
            f"<img src=\"../images/pixelated_posters/{item['file']}\">"
            f"<div class=\"text-container\">"
            f"<span class=\"title\">{item['title']}</span> "
            f"<span class=\"author\">{item['director']}</span> "
            f"<span class=\"year\">{item['year']}</span>"
            f"</div>"
            f"</li>\n"
        )
        currently_watching_content += media_html
    currently_watching_content += "\t\t\t</ul>\n"

    completed_media_content_2024 = ""
    completed_media_content_2025 = ""
    completed_media_content_2024 += "\t\t\t<ul>\n"
    completed_media_content_2025 += "\t\t\t<ul>\n"
    for item in completed_media:
        year = item['date'].year
        media_html = (
            f"\t\t\t\t<li>"
            f"<img src=\"../images/pixelated_posters/{item['file']}\">"
            f"<div class=\"text-container\">"
            f"<span class=\"title\">{item['title']}</span> "
            f"<span class=\"author\">{item['director']}</span> "
            f"<span class=\"year\">{item['year']}</span>"
            f"</div>"
            f"</li>\n"
        )
        if year == 2024:
            completed_media_content_2024 += media_html
        else:
            completed_media_content_2025 += media_html

    completed_media_content_2024 += "\t\t\t</ul>\n"
    completed_media_content_2025 += "\t\t\t</ul>\n"

    update_html(
        "site/html/media.html",
        "<!-- currently_watching_start -->",
        "<!-- currently_watching_end -->",
        currently_watching_content,
    )

    update_html(
        "site/html/media.html",
        "<!-- 2024_consumed_start -->",
        "<!-- 2024_consumed_end -->",
        completed_media_content_2024,
    )

    update_html(
        "site/html/media.html",
        "<!-- 2025_consumed_start -->",
        "<!-- 2025_consumed_end -->",
        completed_media_content_2025,
    )
    
    update_html(
        "site/html/media.html",
        "<!-- navigation_bar_start -->",
        "<!-- navigation_bar_end -->",
        media_navigation_bar,
    )
    
    update_html(
        "site/html/media.html",
        "<!-- head_start -->",
        "<!-- head_end -->",
        media_head,
    )

def generate_bookshelf(website_base_dir):
    
    bookshelf_head = head.replace("styles.css", "../styles.css")
    bookshelf_navigation_bar = navigation_bar.replace("blake's cybernetic canopy", "blake's bookshelf")
    bookshelf_navigation_bar = bookshelf_navigation_bar.replace("index.html", "../index.html")
    bookshelf_navigation_bar = bookshelf_navigation_bar.replace("html/projects.html", "projects.html")
    bookshelf_navigation_bar = bookshelf_navigation_bar.replace("html/bookshelf.html", "bookshelf.html")
    bookshelf_navigation_bar = bookshelf_navigation_bar.replace("html/media.html", "media.html")

    files = os.listdir("../blakelawyer.dev/docs/bookshelf")
    files.remove("template.md")

    books = []
    for file in files:
        metadata, _ = parse_markdown_with_metadata(f"{website_base_dir}/docs/bookshelf/{file}")
        metadata['file'] = file.split(".")[0] + ".jpg"
        books.append(metadata)

    currently_reading = []
    completed_books = []
    for book in books:
        if book['completed']:
            completed_books.append(book)
        else:
            currently_reading.append(book)

    completed_books = sorted(
        completed_books,
        key=lambda x: x['date'],
        reverse=True
    )

    currently_reading_content = ""
    currently_reading_content += "\t\t\t<ul>\n"
    for book in currently_reading:
        book_html = (
            f"\t\t\t\t<li>"
            f"<img src=\"../images/pixelated_covers/{book['file']}\">"
            f"<div class=\"text-container\">"
            f"<span class=\"title\">{book['title']}</span> "
            f"<span class=\"author\">{book['author']}</span> "
            f"<span class=\"year\">{book['year']}</span>"
            f"</div>"
            f"</li>\n"
        ) 
        currently_reading_content += book_html
    currently_reading_content += "\t\t\t</ul>\n"

    completed_books_content_2024 = ""
    completed_books_content_2025 = ""
    completed_books_content_2024 += "\t\t\t<ul>\n"
    completed_books_content_2025 += "\t\t\t<ul>\n"

    for book in completed_books:
        year = book['date'].year

        book_html = (
            f"\t\t\t\t<li>"
            f"<img src=\"../images/pixelated_covers/{book['file']}\">"
            f"<div class=\"text-container\">"
            f"<span class=\"title\">{book['title']}</span> "
            f"<span class=\"author\">{book['author']}</span> "
            f"<span class=\"year\">{book['year']}</span>"
            f"</div>"
            f"</li>\n"
        )
        if year == 2024:
            completed_books_content_2024 += book_html
        else:
            completed_books_content_2025 += book_html

    completed_books_content_2024 += "\t\t\t</ul>\n"
    completed_books_content_2025 += "\t\t\t</ul>\n"
    
    update_html(
        "site/html/bookshelf.html",
        "<!-- currently_reading_start -->",
        "<!-- currently_reading_end -->",
        currently_reading_content,
    )
    
    update_html(
        "site/html/bookshelf.html",
        "<!-- 2024_books_start -->",
        "<!-- 2024_books_end -->",
        completed_books_content_2024,
    )

    update_html(
        "site/html/bookshelf.html",
        "<!-- 2025_books_start -->",
        "<!-- 2025_books_end -->",
        completed_books_content_2025,
    )

    update_html(
        "site/html/bookshelf.html",
        "<!-- navigation_bar_start -->",
        "<!-- navigation_bar_end -->",
        bookshelf_navigation_bar,
    )
    
    update_html(
        "site/html/bookshelf.html",
        "<!-- head_start -->",
        "<!-- head_end -->",
        bookshelf_head,
    )
    
def update_html(html_file, marker_start, marker_end, new_content):

    with open(html_file, 'r') as file:
        html_content = file.read()

    
    start_idx = html_content.find(marker_start) + len(marker_start)
    end_idx = html_content.find(marker_end)
    
    if start_idx != -1 and end_idx != -1:
        updated_html = (
            html_content[:start_idx] +
            '\n' + new_content + '\n' +
            html_content[end_idx:]
        )

        updated_html = updated_html.replace(marker_start, "")
        updated_html = updated_html.replace(marker_end, "")
        
        updated_html = '\n'.join([line for line in updated_html.splitlines() if line.strip() != ""])

        with open(html_file, 'w') as file:
            file.write(updated_html)
    else:
        print("Markers not found!")


def create_site_directory(website_base_dir):

    if os.path.exists("site"):
        shutil.rmtree("site")
    os.makedirs("site")
    os.makedirs("site/html")

    shutil.copy2(f"{website_base_dir}/index.html", "site/index.html")
    shutil.copy2(f"{website_base_dir}/styles.css", "site/styles.css")
    shutil.copy2(f"{website_base_dir}/html/projects.html", "site/html/projects.html")
    shutil.copy2(f"{website_base_dir}/html/bookshelf.html", "site/html/bookshelf.html")
    shutil.copy2(f"{website_base_dir}/html/media.html", "site/html/media.html")
    shutil.copytree(f"{website_base_dir}/images", "site/images")
    
    os.makedirs("site/images/pixelated_covers")
    os.makedirs("site/images/pixelated_posters")


if __name__ =="__main__":
    main()
