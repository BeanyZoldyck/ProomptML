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

        for (const line of lines) {
          const trimmed = line.trim()
          if (!trimmed || trimmed.startsWith("#")) continue

          const spaceIdx = trimmed.indexOf(" ")
          if (spaceIdx === -1) {
            xmlTags.push(`<${trimmed} />`)
          } else {
            const tag = trimmed.slice(0, spaceIdx)
            const content = trimmed.slice(spaceIdx + 1).trim()
            xmlTags.push(`<${tag}>${content}</${tag}>`)
          }
        }

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
