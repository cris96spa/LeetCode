-- Pandoc filter for utils/export_pdf.py: maps docs markup onto header.tex styles.

local KINDS = {
  note = { "adm-note", "\\faInfoCircle" },
  info = { "adm-note", "\\faInfoCircle" },
  abstract = { "adm-note", "\\faClipboard" },
  tip = { "adm-tip", "\\faLightbulb" },
  hint = { "adm-tip", "\\faLightbulb" },
  success = { "adm-tip", "\\faCheckCircle" },
  warning = { "adm-warning", "\\faExclamationTriangle" },
  caution = { "adm-warning", "\\faExclamationTriangle" },
  danger = { "adm-danger", "\\faBolt" },
  bug = { "adm-danger", "\\faBug" },
  question = { "adm-question", "\\faQuestionCircle" },
  example = { "adm-example", "\\faFlask" },
  quote = { "adm-quote", "\\faQuoteLeft" },
}

local function latex(s)
  return pandoc.RawBlock("latex", s)
end

local function inline_latex(markdown)
  local blocks = pandoc.read(markdown, "markdown").blocks
  if #blocks == 0 then
    return ""
  end
  local tex = pandoc.write(pandoc.Pandoc({ pandoc.Plain(blocks[1].content) }), "latex")
  return (tex:gsub("%s+$", ""))
end

function Div(div)
  if not div.classes:includes("admonition") then
    return nil
  end
  local kind = div.classes[2] or "note"
  local style = KINDS[kind] or KINDS.note
  local title = inline_latex(div.attributes.title or (kind:gsub("^%l", string.upper)))
  local out = pandoc.List({ latex(string.format("\\begin{admon}{%s}{%s}{%s}", style[1], style[2], title)) })
  out:extend(div.content)
  out:insert(latex("\\end{admon}"))
  return out
end

-- Unhighlighted blocks (```text) would otherwise be bare verbatim.
function CodeBlock(block)
  local lang = block.classes[1]
  if lang and lang ~= "text" then
    return nil
  end
  -- Escape for commandchars so glyphs missing from the mono font can be swapped in.
  local text = block.text:gsub("[\\{}]", "\\%0"):gsub("\\\\", "\\textbackslash{}"):gsub("★", "\\monostar{}")
  return latex("\\begin{codebox}\\begin{Verbatim}[breaklines, fontsize=\\small, commandchars=\\\\\\{\\}]\n"
    .. text .. "\n\\end{Verbatim}\n\\end{codebox}")
end

function BlockQuote(quote)
  local out = pandoc.List({ latex("\\begin{quotebox}") })
  out:extend(quote.content)
  out:insert(latex("\\end{quotebox}"))
  return out
end

function HorizontalRule()
  return latex("\\sectionrule")
end

function Table(tbl)
  for _, row in ipairs(tbl.head.rows) do
    for _, cell in ipairs(row.cells) do
      cell.contents = cell.contents:walk({
        Plain = function(p)
          return pandoc.Plain({ pandoc.Strong(p.content) })
        end,
      })
    end
  end
  return tbl
end
