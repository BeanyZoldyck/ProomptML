export default {
  id: "xml-prompt",
  async server(input, options) {
    return {
      async "command.execute.before"(input, output) {
        if (input.command !== "xml") return

        const args = input.arguments
        if (!args || !args.trim()) return

        const lines = args.split("\n")
        const xmlTags = []
        let currentTag = null
        let currentContent = []

        const flushCurrentTag = () => {
          if (!currentTag) return

          if (currentContent.length === 0) {
            xmlTags.push(`<${currentTag} />`)
          } else {
            xmlTags.push(`<${currentTag}>${currentContent.join("\n")}</${currentTag}>`)
          }

          currentTag = null
          currentContent = []
        }

        const parseTagLine = (line) => {
          const trimmed = line.trim()
          const hasPrefix = trimmed.startsWith("/")
          const source = hasPrefix ? trimmed.slice(1).trim() : trimmed

          if (!source) return null

          const spaceIdx = source.indexOf(" ")
          if (spaceIdx === -1) {
            return { tag: source, firstContent: "" }
          }

          const firstContent = source.slice(spaceIdx + 1).trim()

          return {
            tag: source.slice(0, spaceIdx),
            firstContent:
              hasPrefix && firstContent.endsWith("/")
                ? firstContent.slice(0, -1).trimEnd()
                : firstContent,
          }
        }

        for (const line of lines) {
          const trimmed = line.trim()

          if (!trimmed || trimmed.startsWith("#")) {
            if (currentTag && !trimmed.startsWith("#")) {
              currentContent.push("")
            }
            continue
          }

          if (trimmed.startsWith("/")) {
            const parsed = parseTagLine(line)
            if (!parsed) continue

            flushCurrentTag()
            currentTag = parsed.tag
            if (parsed.firstContent) currentContent.push(parsed.firstContent)
            continue
          }

          if (!currentTag) {
            const parsed = parseTagLine(line)
            if (!parsed) continue

            currentTag = parsed.tag
            if (parsed.firstContent) currentContent.push(parsed.firstContent)
            continue
          }

          currentContent.push(trimmed)
        }

        flushCurrentTag()

        if (xmlTags.length === 0) return

        const xml = xmlTags.join("\n")

        for (const part of output.parts) {
          if (part.type === "text") {
            part.text = xml
            return
          }
        }

        output.parts.push({ type: "text", text: xml })
      },
    }
  },
}
