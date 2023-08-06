from notion.client import NotionClient

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
client = NotionClient(token_v2="be91ccf5d30fd1bfbae2ed99803a99b1b5d9e4ede055b41e34a8b4e49586f783ba3eedfcaa3d5aea397cf9cdc787a2ee6d4802e3dff7d17b6c60f408beded6bc5fd5c6c75957a60ee82306250085")

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/pplink/70ec5b5022224a11950acbb63dd96692?v=0bc2a497051442bcbe4d3ff104675f22")

print("The old title is:", page.title)

# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
page.title = "The title has now changed, and has *live-uㄴted* in the browser!"