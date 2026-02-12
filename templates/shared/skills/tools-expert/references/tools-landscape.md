# CrewAI Tools Landscape

## Scope and Sources

- Primary docs index: `https://docs.crewai.com/en/tools/overview`
- Category overviews: File & Document, Web Scraping, Search & Research, Database & Data, AI & ML, Cloud & Storage, Integration, Automation
- Custom tools guide: `https://docs.crewai.com/en/learn/create-custom-tools`
- Concepts guide: `https://docs.crewai.com/en/concepts/tools`
- Repository snapshot via zread MCP: `crewAIInc/crewAI-tools`

Note: The `crewAIInc/crewAI-tools` repository is marked deprecated in its README and points to the maintained monorepo path: `crewAIInc/crewAI/tree/main/lib/crewai-tools`.

## Category-to-Intent Quick Map

| Intent | Start Here | Typical Tools |
| --- | --- | --- |
| Read/search local documents | File & Document | `FileReadTool`, `DirectoryReadTool`, RAG document tools |
| Scrape or automate websites | Web Scraping | `ScrapeWebsiteTool`, `SeleniumScrapingTool`, Firecrawl family |
| General internet research | Search & Research | `SerperDevTool`, `BraveSearchTool`, `TavilySearchTool` |
| Query SQL/vector stores | Database & Data | `MySQLSearchTool`, `PGSearchTool`, `QdrantVectorSearchTool` |
| Run AI-specific operations | AI & ML | `CodeInterpreterTool`, `DallETool`, `VisionTool` |
| Use cloud storage/services | Cloud & Storage | `S3ReaderTool`, `S3WriterTool`, Bedrock KB tool |
| Invoke external automations | Integration | `InvokeCrewAIAutomationTool`, `BedrockInvokeAgentTool` |
| Connect third-party platforms | Automation | `ApifyActorsTool`, `ComposioTool`, `ZapierActions` adapter |

## Built-In Categories and Tools (Docs-Aligned)

### File & Document

- `FileReadTool`
- `FileWriterTool`
- `PDFSearchTool`
- `DOCXSearchTool`
- `MDXSearchTool`
- `XMLSearchTool`
- `TXTSearchTool`
- `JSONSearchTool`
- `CSVSearchTool`
- `DirectorySearchTool`
- `DirectoryReadTool`
- `OCRTool`
- `PDFTextWritingTool`

### Web Scraping & Browsing

- `ScrapeWebsiteTool`
- `ScrapeElementFromWebsiteTool`
- `FirecrawlCrawlWebsiteTool`
- `FirecrawlScrapeWebsiteTool`
- `FirecrawlSearchTool`
- `SeleniumScrapingTool`
- `ScrapflyScrapeWebsiteTool`
- `ScrapegraphScrapeTool`
- `SpiderTool`
- `BrowserbaseLoadTool`
- `HyperbrowserLoadTool`
- `StagehandTool`
- Bright Data tool family
- Oxylabs scraper family

### Search & Research

- `SerperDevTool`
- `BraveSearchTool`
- `EXASearchTool`
- `LinkupSearchTool`
- `GithubSearchTool`
- `WebsiteSearchTool`
- `CodeDocsSearchTool`
- `YoutubeChannelSearchTool`
- `YoutubeVideoSearchTool`
- `TavilySearchTool`
- `TavilyExtractorTool`
- `ArxivPaperTool`
- `SerpApiGoogleSearchTool`
- `SerpApiGoogleShoppingTool`
- `DatabricksQueryTool`

### Database & Data

- `MySQLSearchTool`
- `PGSearchTool`
- `SnowflakeSearchTool`
- `NL2SQLTool`
- `QdrantVectorSearchTool`
- `WeaviateVectorSearchTool`
- `MongoDBVectorSearchTool`
- `SingleStoreSearchTool`

### AI & Machine Learning

- `DallETool`
- `VisionTool`
- `AIMindTool`
- `LlamaIndexTool`
- `LangChainTool`
- `RagTool`
- `CodeInterpreterTool`

### Cloud & Storage

- `S3ReaderTool`
- `S3WriterTool`
- Bedrock Knowledge Base retriever tool

### Integration

- `MergeAgentHandlerTool`
- `InvokeCrewAIAutomationTool`
- `BedrockInvokeAgentTool`

### Automation

- `ApifyActorsTool`
- `ComposioTool`
- `MultiOnTool`
- `ZapierActionsAdapter`

## Additional Families Found in zread Repository Structure

The following folders appear in `crewai_tools/tools/` and may expose tools that are less prominent in docs navigation:

- `contextualai_*` tool family
- `crewai_enterprise_tools`
- `crewai_platform_tools`
- `jina_scrape_website_tool`
- `serply_api_tool`
- `parallel_tools`
- `nl2sql`
- `rag` submodule

Treat these as implementation inventory and verify current support in the maintained monorepo before relying on them in production.

## Common Configuration Patterns

- Search APIs: `SERPER_API_KEY`, Brave/Tavily/SerpApi keys
- Cloud storage: AWS credentials and region variables
- Browser automation services: provider-specific API keys
- Database tools: host/user/password/database and optional SSL settings
- Integration tools: bearer tokens or provider credentials

## Fast Selection Patterns

- Need quick web facts with low setup: start with `SerperDevTool`
- Need privacy-friendly search: prefer `BraveSearchTool`
- Need rich site extraction at scale: prefer Firecrawl or Scrapfly families
- Need semantic retrieval from files: prefer document RAG tools (`PDFSearchTool`, `DOCXSearchTool`, etc.)
- Need SQL from natural language: use `NL2SQLTool` with DB access tools
- Need Python execution and transformations: use `CodeInterpreterTool`
- Need external workflow handoff: use integration/automation tools instead of custom HTTP glue code
