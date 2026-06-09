import sys

def inject_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    css_injection = """
    <link rel="stylesheet" href="./css/design_system.css">
    <link rel="stylesheet" href="./css/resume_intelligence.css">
    """
    
    js_injection = """
    <script src="./js/ResumeService.js"></script>
    <script src="./js/ResumeDashboard.js"></script>
    """

    if "</head>" in content:
        content = content.replace("</head>", css_injection + "\n</head>")
    
    if "</body>" in content:
        content = content.replace("</body>", js_injection + "\n</body>")
    else:
        content += js_injection

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    inject_tags(sys.argv[1])
