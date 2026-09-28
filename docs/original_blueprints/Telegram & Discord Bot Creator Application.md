---
fable_schema: "5.1.0"
urn: "urn:tgn:blueprint:visual_builder:44301e97-5eec-4302-8af9-d34361791295"
title: "Multi-Platform Visual Bot Creator Studio Specification"
transport: "HybridBridge"
concurrency:
  paradigm: "AsyncIO"
  max_throughput_est: "1000 req/s"
fsm:
  defined: true
  states:
    - "NODE_INITIALIZED"
    - "CANVAS_EDITING"
    - "SYNTAX_VALIDATING"
    - "CONTAINER_PROVISIONING"
    - "DEPLOYING"
    - "ACTIVE"
    - "PAUSED"
  storage_driver: "SQL"
dependencies:
  external:
    - "next>=14.0.0"
    - "react>=18.2.0"
    - "prisma>=5.0.0"
    - "fastapi>=0.100.0"
    - "docker>=6.1.0"
    - "pydantic>=2.0"
  internal_urns:
    - "urn:tgn:blueprint:core_architecture:c91326b5-0ac7-4543-83f6-54bcbc855c1b"
    - "urn:tgn:blueprint:root_manifest:b3356305-5168-4c19-a781-afebcf4d07bf"
breaking_changes_detected:
  - "Next.js 14 App Router migration from Pages Router"
  - "Prisma client edge runtime restrictions"
verification_checksum: "be29b3f314ef4e6e28c47bfea0ec50bbcecc8cbafd57551f784c698877eb7b65"
---
# Sophisticated Prompt for Gemini AI Studio
## Telegram & Discord Bot Creator Application

---

```markdown
# SYSTEM ROLE & CONTEXT

You are an expert full-stack developer and software architect specializing in bot development, API integrations, and developer tools. Your task is to design and build a comprehensive, production-ready Bot Creator Application that enables users to create, configure, deploy, and manage bots for both Telegram and Discord platforms without extensive coding knowledge.

---

# PROJECT SPECIFICATION

## 🎯 PRIMARY OBJECTIVE

Build a sophisticated, modular Bot Creator Application with the following core capabilities:

1. **Visual Bot Builder** - Drag-and-drop interface for creating bot logic
2. **Code Editor** - Advanced IDE-like environment for custom scripting
3. **Multi-Platform Support** - Unified interface for Telegram and Discord bots
4. **Template Library** - Pre-built bot templates for common use cases
5. **Real-time Testing** - Live preview and debugging environment
6. **Deployment Pipeline** - One-click deployment with hosting options

---

## 🏗️ TECHNICAL ARCHITECTURE

### Technology Stack

```yaml
Frontend:
  Framework: React 18+ with TypeScript
  State Management: Zustand or Redux Toolkit
  UI Library: Tailwind CSS + shadcn/ui
  Visual Builder: React Flow or Rete.js
  Code Editor: Monaco Editor (VS Code engine)

Backend:
  Runtime: Node.js 20+ with Express/Fastify
  Language: TypeScript
  Database: PostgreSQL (primary) + Redis (caching/sessions)
  ORM: Prisma or Drizzle
  Queue System: Bull MQ for job processing

Bot Engines:
  Telegram: grammy or telegraf library
  Discord: discord.js v14+
  
Infrastructure:
  Containerization: Docker + Docker Compose
  Process Manager: PM2
  Reverse Proxy: Nginx
  WebSocket: Socket.io for real-time updates
```

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Visual Builder│  │ Code Editor  │  │ Dashboard & Analytics│  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API GATEWAY                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ Auth Service│  │ Bot Manager │  │ Template API│  │ Analytics │ │
│  └────────────┘  └────────────┘  └────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BOT EXECUTION LAYER                         │
│  ┌─────────────────────┐      ┌─────────────────────┐          │
│  │  Telegram Runtime   │      │   Discord Runtime    │          │
│  │  ┌───────────────┐  │      │  ┌───────────────┐  │          │
│  │  │ Bot Instance 1│  │      │  │ Bot Instance 1│  │          │
│  │  │ Bot Instance 2│  │      │  │ Bot Instance 2│  │          │
│  │  │ Bot Instance N│  │      │  │ Bot Instance N│  │          │
│  │  └───────────────┘  │      │  └───────────────┘  │          │
│  └─────────────────────┘      └─────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ PostgreSQL │  │   Redis    │  │  S3/MinIO  │  │  Logging  │ │
│  └────────────┘  └────────────┘  └────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 FEATURE REQUIREMENTS

### 1. User Management & Authentication

```typescript
interface AuthenticationSystem {
  methods: ['email/password', 'OAuth2 (Google, GitHub, Discord)'];
  features: {
    mfa: 'TOTP-based two-factor authentication';
    sessions: 'JWT with refresh token rotation';
    rbac: 'Role-based access control (Admin, Developer, Viewer)';
    apiKeys: 'Secure API key generation for external integrations';
  };
}
```

### 2. Visual Bot Builder

Create an intuitive node-based visual programming interface:

```typescript
interface VisualBuilderNodes {
  triggers: [
    'OnMessage',
    'OnCommand',
    'OnJoin',
    'OnLeave',
    'OnReaction',
    'OnSchedule',
    'OnWebhook',
    'OnButtonClick',
    'OnSlashCommand'
  ];
  
  actions: [
    'SendMessage',
    'SendEmbed',
    'SendMedia',
    'EditMessage',
    'DeleteMessage',
    'AddReaction',
    'BanUser',
    'KickUser',
    'AssignRole',
    'CreateChannel',
    'HTTPRequest',
    'DatabaseQuery',
    'SetVariable',
    'CallFunction'
  ];
  
  logic: [
    'Condition (If/Else)',
    'Switch',
    'Loop',
    'Delay',
    'RandomChoice',
    'RateLimiter',
    'ErrorHandler',
    'ParallelExecution'
  ];
  
  integrations: [
    'OpenAI/Gemini API',
    'Database CRUD',
    'External Webhooks',
    'Email Sender',
    'File Storage',
    'Payment Gateways'
  ];
}
```

### 3. Code Editor Module

```typescript
interface CodeEditorFeatures {
  language: 'TypeScript';
  capabilities: {
    intellisense: 'Full autocomplete with bot API documentation';
    linting: 'ESLint integration with custom rules';
    formatting: 'Prettier auto-formatting';
    snippets: 'Pre-built code snippets for common patterns';
    debugging: 'Breakpoints, variable inspection, call stack';
    versionControl: 'Built-in Git integration';
    collaboration: 'Real-time collaborative editing';
  };
  
  sdkProvided: {
    telegram: 'Wrapped Grammy/Telegraf with enhanced utilities';
    discord: 'Wrapped discord.js with helper functions';
    common: 'Database, HTTP, caching, logging utilities';
  };
}
```

### 4. Template Library

Provide production-ready templates:

```yaml
Telegram Templates:
  - Welcome Bot (greets new members, rules, verification)
  - Moderation Bot (anti-spam, word filters, warnings)
  - FAQ Bot (inline queries, keyboard menus)
  - E-commerce Bot (product catalog, cart, payments)
  - Notification Bot (RSS feeds, scheduled messages)
  - Poll & Survey Bot
  - File Manager Bot
  - AI Assistant Bot (Gemini/OpenAI integration)

Discord Templates:
  - Server Management Bot (autorole, logging, tickets)
  - Music Bot (YouTube, Spotify integration)
  - Leveling System Bot (XP, ranks, leaderboards)
  - Giveaway Bot
  - Reaction Roles Bot
  - Verification Bot (CAPTCHA, phone verification)
  - Economy Bot (currency, shop, gambling)
  - AI Chatbot
  - Moderation Suite
  - Custom Commands Bot
```

### 5. Bot Configuration Interface

```typescript
interface BotConfiguration {
  general: {
    name: string;
    description: string;
    avatar: File;
    platform: 'telegram' | 'discord' | 'both';
    status: 'online' | 'idle' | 'dnd' | 'invisible';
  };
  
  telegram: {
    token: string; // encrypted storage
    webhookUrl?: string;
    allowedUpdates: UpdateType[];
    commands: BotCommand[];
    inlineMode: boolean;
    groupPrivacy: boolean;
  };
  
  discord: {
    token: string; // encrypted storage
    clientId: string;
    clientSecret: string;
    intents: GatewayIntentBits[];
    slashCommands: SlashCommand[];
    permissions: PermissionsBitField;
  };
  
  advanced: {
    rateLimiting: RateLimitConfig;
    errorHandling: ErrorHandlingConfig;
    logging: LoggingConfig;
    caching: CacheConfig;
    database: DatabaseConfig;
  };
}
```

### 6. Deployment & Hosting

```typescript
interface DeploymentOptions {
  managed: {
    description: 'One-click deployment to our infrastructure';
    features: ['Auto-scaling', 'SSL', 'Monitoring', '99.9% uptime'];
    tiers: ['Free (limited)', 'Pro', 'Enterprise'];
  };
  
  selfHosted: {
    docker: 'Docker image with docker-compose setup';
    kubernetes: 'Helm charts for K8s deployment';
    serverless: 'AWS Lambda / Google Cloud Functions templates';
    vps: 'Installation scripts for Ubuntu/Debian';
  };
  
  cicd: {
    github: 'GitHub Actions workflow templates';
    gitlab: 'GitLab CI/CD configuration';
    bitbucket: 'Bitbucket Pipelines setup';
  };
}
```

### 7. Analytics & Monitoring Dashboard

```typescript
interface AnalyticsDashboard {
  metrics: {
    usage: ['Messages processed', 'Commands executed', 'Users served'];
    performance: ['Response time', 'Uptime', 'Error rate'];
    growth: ['New users', 'Active users', 'Retention'];
    engagement: ['Popular commands', 'Peak hours', 'User flows'];
  };
  
  monitoring: {
    realTime: 'Live message/event stream';
    alerts: 'Configurable alerts (email, webhook, SMS)';
    logs: 'Searchable log aggregation';
    tracing: 'Request tracing and debugging';
  };
  
  reporting: {
    scheduled: 'Daily/weekly/monthly reports';
    export: 'CSV, JSON, PDF export';
    api: 'Programmatic access to analytics data';
  };
}
```

---

## 💾 DATABASE SCHEMA

```prisma
// Prisma Schema

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  passwordHash  String?
  name          String?
  avatar        String?
  role          Role      @default(USER)
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  bots          Bot[]
  teams         TeamMember[]
  apiKeys       ApiKey[]
  sessions      Session[]
}

model Team {
  id          String       @id @default(cuid())
  name        String
  createdAt   DateTime     @default(now())
  
  members     TeamMember[]
  bots        Bot[]
}

model TeamMember {
  id        String   @id @default(cuid())
  userId    String
  teamId    String
  role      TeamRole @default(MEMBER)
  joinedAt  DateTime @default(now())
  
  user      User     @relation(fields: [userId], references: [id])
  team      Team     @relation(fields: [teamId], references: [id])
  
  @@unique([userId, teamId])
}

model Bot {
  id              String      @id @default(cuid())
  name            String
  description     String?
  platform        Platform
  status          BotStatus   @default(STOPPED)
  
  // Encrypted credentials
  telegramToken   String?
  discordToken    String?
  discordClientId String?
  
  // Configuration
  config          Json        @default("{}")
  flowData        Json?       // Visual builder data
  customCode      String?     // Custom TypeScript code
  
  // Metadata
  createdAt       DateTime    @default(now())
  updatedAt       DateTime    @updatedAt
  lastDeployedAt  DateTime?
  
  // Relations
  ownerId         String
  owner           User        @relation(fields: [ownerId], references: [id])
  teamId          String?
  team            Team?       @relation(fields: [teamId], references: [id])
  
  commands        Command[]
  variables       Variable[]
  logs            BotLog[]
  analytics       Analytics[]
  deployments     Deployment[]
  webhooks        Webhook[]
}

model Command {
  id          String      @id @default(cuid())
  botId       String
  name        String
  description String?
  trigger     String      // e.g., "/start", "!help"
  type        CommandType
  response    Json        // Can be text, embed, or complex flow
  enabled     Boolean     @default(true)
  
  bot         Bot         @relation(fields: [botId], references: [id], onDelete: Cascade)
  
  @@unique([botId, trigger])
}

model Variable {
  id        String   @id @default(cuid())
  botId     String
  name      String
  value     Json
  scope     VariableScope @default(GLOBAL)
  
  bot       Bot      @relation(fields: [botId], references: [id], onDelete: Cascade)
  
  @@unique([botId, name])
}

model BotLog {
  id        String   @id @default(cuid())
  botId     String
  level     LogLevel
  message   String
  metadata  Json?
  timestamp DateTime @default(now())
  
  bot       Bot      @relation(fields: [botId], references: [id], onDelete: Cascade)
  
  @@index([botId, timestamp])
}

model Analytics {
  id              String   @id @default(cuid())
  botId           String
  date            DateTime @db.Date
  messagesCount   Int      @default(0)
  commandsCount   Int      @default(0)
  uniqueUsers     Int      @default(0)
  errorsCount     Int      @default(0)
  avgResponseTime Float?
  
  bot             Bot      @relation(fields: [botId], references: [id], onDelete: Cascade)
  
  @@unique([botId, date])
}

model Deployment {
  id          String           @id @default(cuid())
  botId       String
  version     String
  status      DeploymentStatus
  environment String           @default("production")
  config      Json
  logs        String?
  createdAt   DateTime         @default(now())
  completedAt DateTime?
  
  bot         Bot              @relation(fields: [botId], references: [id], onDelete: Cascade)
}

model Template {
  id          String   @id @default(cuid())
  name        String
  description String
  platform    Platform
  category    String
  thumbnail   String?
  flowData    Json
  customCode  String?
  config      Json
  isPublic    Boolean  @default(true)
  downloads   Int      @default(0)
  rating      Float?
  createdAt   DateTime @default(now())
}

model ApiKey {
  id          String   @id @default(cuid())
  userId      String
  name        String
  keyHash     String   @unique
  lastUsedAt  DateTime?
  expiresAt   DateTime?
  permissions Json     @default("[]")
  createdAt   DateTime @default(now())
  
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model Session {
  id           String   @id @default(cuid())
  userId       String
  refreshToken String   @unique
  userAgent    String?
  ipAddress    String?
  expiresAt    DateTime
  createdAt    DateTime @default(now())
  
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model Webhook {
  id        String   @id @default(cuid())
  botId     String
  name      String
  url       String   @unique
  secret    String
  events    String[]
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())
  
  bot       Bot      @relation(fields: [botId], references: [id], onDelete: Cascade)
}

// Enums
enum Role {
  USER
  ADMIN
  SUPER_ADMIN
}

enum TeamRole {
  OWNER
  ADMIN
  MEMBER
  VIEWER
}

enum Platform {
  TELEGRAM
  DISCORD
  BOTH
}

enum BotStatus {
  RUNNING
  STOPPED
  ERROR
  DEPLOYING
  MAINTENANCE
}

enum CommandType {
  TEXT
  EMBED
  FLOW
  CUSTOM
}

enum VariableScope {
  GLOBAL
  USER
  GUILD
  CHANNEL
}

enum LogLevel {
  DEBUG
  INFO
  WARN
  ERROR
  FATAL
}

enum DeploymentStatus {
  PENDING
  IN_PROGRESS
  SUCCESS
  FAILED
  ROLLED_BACK
}
```

---

## 🔐 SECURITY REQUIREMENTS

```typescript
interface SecurityMeasures {
  encryption: {
    atRest: 'AES-256 for sensitive data (tokens, secrets)';
    inTransit: 'TLS 1.3 for all communications';
    keys: 'AWS KMS or HashiCorp Vault for key management';
  };
  
  authentication: {
    passwords: 'Argon2id hashing with salt';
    tokens: 'JWT with RS256, short expiry, refresh rotation';
    mfa: 'TOTP with backup codes';
  };
  
  authorization: {
    rbac: 'Role-based access with fine-grained permissions';
    resourceLevel: 'Bot-level and team-level access control';
    apiScopes: 'Scoped API keys with minimal permissions';
  };
  
  protection: {
    rateLimit: 'Per-user and per-endpoint rate limiting';
    ddos: 'Cloudflare or similar DDoS protection';
    injection: 'Parameterized queries, input sanitization';
    xss: 'Content Security Policy, output encoding';
    csrf: 'Token-based CSRF protection';
  };
  
  audit: {
    logging: 'Comprehensive audit logs for all actions';
    monitoring: 'Real-time security event monitoring';
    alerts: 'Automated alerts for suspicious activity';
  };
  
  compliance: {
    gdpr: 'Data export, deletion, consent management';
    dataResidency: 'Regional data storage options';
  };
}
```

---

## 📁 PROJECT STRUCTURE

```
bot-creator-app/
├── apps/
│   ├── web/                          # Frontend React application
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── builder/          # Visual bot builder components
│   │   │   │   ├── editor/           # Code editor components
│   │   │   │   ├── dashboard/        # Dashboard widgets
│   │   │   │   ├── common/           # Shared UI components
│   │   │   │   └── layout/           # Layout components
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── stores/               # Zustand stores
│   │   │   ├── services/             # API services
│   │   │   ├── types/
│   │   │   └── utils/
│   │   ├── public/
│   │   └── package.json
│   │
│   ├── api/                          # Backend API server
│   │   ├── src/
│   │   │   ├── modules/
│   │   │   │   ├── auth/
│   │   │   │   ├── bots/
│   │   │   │   ├── users/
│   │   │   │   ├── teams/
│   │   │   │   ├── templates/
│   │   │   │   ├── analytics/
│   │   │   │   └── deployments/
│   │   │   ├── middleware/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   └── config/
│   │   └── package.json
│   │
│   └── bot-runner/                   # Bot execution runtime
│       ├── src/
│       │   ├── engines/
│       │   │   ├── telegram/
│       │   │   └── discord/
│       │   ├── interpreters/         # Flow interpreter
│       │   ├── sandbox/              # Secure code execution
│       │   └── managers/
│       └── package.json
│
├── packages/
│   ├── shared/                       # Shared types and utilities
│   │   ├── src/
│   │   │   ├── types/
│   │   │   ├── validators/
│   │   │   └── constants/
│   │   └── package.json
│   │
│   ├── bot-sdk/                      # Bot development SDK
│   │   ├── src/
│   │   │   ├── telegram/
│   │   │   ├── discord/
│   │   │   ├── database/
│   │   │   └── utilities/
│   │   └── package.json
│   │
│   └── ui/                           # Shared UI component library
│       ├── src/
│       │   ├── components/
│       │   ├── hooks/
│       │   └── styles/
│       └── package.json
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile.web
│   │   ├── Dockerfile.api
│   │   ├── Dockerfile.runner
│   │   └── docker-compose.yml
│   ├── kubernetes/
│   │   └── helm/
│   └── terraform/
│
├── docs/
│   ├── api/
│   ├── guides/
│   └── sdk/
│
├── scripts/
├── .github/
│   └── workflows/
├── turbo.json                        # Turborepo configuration
├── package.json
└── README.md
```

---

## 🎨 UI/UX SPECIFICATIONS

### Design System

```typescript
interface DesignSystem {
  theme: {
    mode: 'light' | 'dark' | 'system';
    colors: {
      primary: '#6366F1';      // Indigo
      secondary: '#8B5CF6';    // Violet
      telegram: '#0088CC';     // Telegram blue
      discord: '#5865F2';      // Discord blurple
      success: '#10B981';
      warning: '#F59E0B';
      error: '#EF4444';
      neutral: 'Slate scale';
    };
    typography: {
      fontFamily: 'Inter, system-ui, sans-serif';
      monoFamily: 'JetBrains Mono, monospace';
    };
  };
  
  components: {
    buttons: 'Primary, Secondary, Ghost, Danger variants';
    inputs: 'Text, Select, Checkbox, Radio, Toggle, Range';
    cards: 'Elevated, Outlined, Interactive';
    modals: 'Dialog, Drawer, Command Palette';
    navigation: 'Sidebar, Tabs, Breadcrumbs';
    feedback: 'Toast, Alert, Progress, Skeleton';
  };
  
  patterns: {
    forms: 'React Hook Form with Zod validation';
    tables: 'TanStack Table with sorting, filtering, pagination';
    lists: 'Virtualized lists for performance';
    dragDrop: 'DnD Kit for drag and drop';
  };
}
```

### Key Screens

1. **Dashboard** - Overview of all bots, quick stats, recent activity
2. **Bot Builder** - Visual flow editor with node palette
3. **Code Editor** - Full-featured IDE with file explorer
4. **Command Manager** - CRUD interface for bot commands
5. **Settings** - Bot configuration, credentials, advanced settings
6. **Analytics** - Charts, metrics, logs viewer
7. **Templates** - Template gallery with search and filters
8. **Team Management** - Member list, roles, invitations
9. **Deployment** - Deployment history, environment management

---

## 📝 IMPLEMENTATION GUIDELINES

### Code Quality Standards

```yaml
TypeScript:
  - Strict mode enabled
  - No 'any' types (use 'unknown' with type guards)
  - Comprehensive JSDoc comments
  - Barrel exports for clean imports

Testing:
  - Unit tests: Vitest with >80% coverage
  - Integration tests: Supertest for API
  - E2E tests: Playwright
  - Visual regression: Chromatic

Documentation:
  - OpenAPI 3.0 spec for all endpoints
  - Storybook for UI components
  - README for each package
  - Architecture Decision Records (ADRs)

Git Workflow:
  - Conventional commits
  - Feature branches
  - Required PR reviews
  - CI checks before merge
```

### Performance Requirements

```yaml
Frontend:
  - Lighthouse score >90
  - First Contentful Paint <1.5s
  - Time to Interactive <3s
  - Bundle size <500KB (gzipped)

Backend:
  - API response time <100ms (p95)
  - Support 1000+ concurrent connections
  - Database queries <50ms

Bot Runtime:
  - Message processing <50ms
  - Support 100+ bots per instance
  - Graceful degradation under load
```

---

## 🚀 DELIVERABLES

Please generate the following:

1. **Complete source code** for all modules with inline comments
2. **API documentation** in OpenAPI format
3. **Database migrations** and seed data
4. **Docker configuration** for local development
5. **Environment configuration** template with all required variables
6. **Unit tests** for critical business logic
7. **User guide** for the visual builder
8. **SDK documentation** for custom bot development
9. **Deployment guide** for self-hosting
10. **Security checklist** and best practices

---

## 🔄 ITERATION INSTRUCTIONS

Start by generating:

1. First, the **core data models and database schema**
2. Then, the **authentication and user management system**
3. Followed by the **bot CRUD operations and configuration**
4. Then, the **visual builder flow interpreter**
5. Finally, the **bot runtime engines for Telegram and Discord**

After each section, pause for feedback before proceeding to the next module.

---

## ⚠️ CONSTRAINTS & CONSIDERATIONS

- Prioritize security - all tokens and secrets must be encrypted
- Ensure scalability - design for horizontal scaling from the start
- Maintain platform parity - features should work identically on both platforms where applicable
- Consider offline capabilities - queue messages when connectivity is lost
- Implement proper error handling - never expose internal errors to users
- Follow rate limits - respect Telegram and Discord API limits
- Enable observability - structured logging, metrics, tracing throughout

---

## 💡 ADDITIONAL CONTEXT

This application should be suitable for:
- Individual developers building personal bots
- Small businesses automating customer interactions
- Communities managing their Telegram/Discord servers
- Enterprises requiring custom bot solutions

The target users range from non-technical users (visual builder) to experienced developers (code editor), so the UI should accommodate both skill levels.

---

BEGIN IMPLEMENTATION
```

---

## Usage Instructions

1. **Copy the entire prompt** above into Gemini AI Studio
2. **Set the model** to Gemini 1.5 Pro or Ultra for best results
3. **Configure temperature** to 0.3-0.4 for more consistent code generation
4. **Use structured output** if generating JSON/code files
5. **Iterate in sections** - ask for specific modules one at a time for better quality

---

Would you like me to expand on any specific section or provide additional prompts for specific features?