# Metaphoric

This repo will contain my blog, alongside with the files required to generate it.
I'll once again use it to experiment with some technologies I'm not familiar with.

# Format specification
Each post consists of one Markdown file, containing the entire post's content.
A posts' filename includes its published date; which determines the order of the posts. The filename (without the date)
is also used as the post's slug / link. To create a draft post, just use the extension ".draft.md".
Each post has to start with a "# header" (can't be an == header, harder to parse), which will be used as the
 post's title. This header has to be on the first line.