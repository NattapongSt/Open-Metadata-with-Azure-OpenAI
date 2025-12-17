allowed_tools = {
    # === Data Assets (24 tools) ===
    # Tables (5)
    'list_tables',
    'get_table',
    'get_table_by_name',
    'create_table',
    'update_table',
    
    # Databases (5)
    'list_databases',
    'get_database',
    'get_database_by_name',
    'create_database',
    'update_database',
    
    # Schemas (5)
    'list_schemas',
    'get_schema',
    'get_schema_by_name',
    'create_schema',
    'update_schema',
    
    # Dashboards (5)
    'list_dashboards',
    'get_dashboard',
    'get_dashboard_by_name',
    'create_dashboard',
    'update_dashboard',
    
    # Charts (4)
    'list_charts',
    'get_chart',
    'get_chart_by_name',
    'create_chart',
    
    # === Data Pipeline & Integration (14 tools) ===
    # Pipelines (5)
    'list_pipelines',
    'get_pipeline',
    'get_pipeline_by_name',
    'create_pipeline',
    'update_pipeline',
    
    # Topics (5)
    'list_topics',
    'get_topic',
    'get_topic_by_name',
    'create_topic',
    'update_topic',
    
    # Containers (4)
    'list_containers',
    'get_container',
    'get_container_by_name',
    'create_container',
    
    # === Analytics & ML (10 tools) ===
    # Metrics (5)
    'list_metrics',
    'get_metric',
    'get_metric_by_name',
    'create_metric',
    'update_metric',
    
    # ML Models (5)
    'list_ml_models',
    'get_ml_model',
    'get_ml_model_by_name',
    'create_ml_model',
    'update_ml_model',
    
    # === User & Access Management (15 tools) ===
    # Users (5)
    'list_users',
    'get_user',
    'get_user_by_name',
    'create_user',
    'update_user',
    
    # Teams (5)
    'list_teams',
    'get_team',
    'get_team_by_name',
    'create_team',
    'update_team',
    
    # Roles (5)
    'list_roles',
    'get_role',
    'get_role_by_name',
    'create_role',
    'update_role',
    
    # === Metadata & Governance (20 tools) ===
    # Tags (6)
    'list_tags',
    'get_tag',
    'get_tag_by_name',
    'create_tag',
    'update_tag',
    'list_tag_categories',
    
    # Glossaries (5)
    'list_glossaries',
    'get_glossary',
    'get_glossary_by_name',
    'create_glossary',
    'update_glossary',
    
    # Glossary Terms (2)
    'list_glossary_terms',
    'get_glossary_term',
    
    # Classifications (4)
    'list_classifications',
    'get_classification',
    'get_classification_by_name',
    'create_classification',
    
    # Policies (3)
    'list_policies',
    'get_policy',
    'get_policy_by_name',
    
    # === Data Lineage & Usage (7 tools) ===
    'get_lineage',
    'get_lineage_by_name',
    'add_lineage',
    'delete_lineage',
    'get_usage_by_entity',
    'add_usage_data',
    'get_entity_usage_summary',
    
    # === Search & Discovery (3 tools) ===
    'search_entities',
    'suggest_entities',
    'search_aggregate',
    
    # === Data Quality & Testing (9 tools) ===
    # Test Cases (4)
    'list_test_cases',
    'get_test_case',
    'get_test_case_by_name',
    'create_test_case',
    
    # Test Suites (4)
    'list_test_suites',
    'get_test_suite',
    'create_basic_test_suite',
    'update_test_suite',
    
    # Quality Reports (1)
    'get_data_quality_report',
    
    # === Service Management (6 tools) ===
    'list_database_services',
    'get_database_service',
    'get_database_service_by_name',
    'list_dashboard_services',
    'get_dashboard_service',
    'test_service_connection',
    
    # === Events & Notifications (6 tools) ===
    'list_events',
    'list_event_subscriptions',
    'get_event_subscription',
    'create_event_subscription',
    'update_event_subscription',
    'delete_event_subscription',
    
    # === Domain & Data Products (8 tools) ===
    # Domains (4)
    'list_domains',
    'get_domain',
    'get_domain_by_name',
    'create_domain',
    
    # Data Products (4)
    'list_data_products',
    'get_data_product',
    'get_data_product_by_name',
    'create_data_product',
    
    # === Reports & Bots (6 tools) ===
    'list_reports',
    'get_report',
    'get_report_by_name',
    'list_bots',
    'get_bot',
    'get_bot_by_name',
}

# สร้าง FQN เองทำให้ดึงข้อมูลไม่ได้
# sys_prompt = """
#         You are a Metadata Intelligence Assistant connected to an OpenMetadata system 
#         via the Model Context Protocol (MCP). 
        
#         You can only access and respond based on data retrieved from the MCP Server using 
#         the available MCP tools. You MUST NOT use any external knowledge or assumptions.

#         Objectives:
#         1.  Answer ONLY using data retrieved from the MCP tools.
#         2.  **Always respond in Thai** unless the user explicitly requests English.
#         3.  If multiple results are found, describe ALL of them.
#         4.  If data is not found, say: "No data found in OpenMetadata."
#         5. Maintain total token usage under 128,000 tokens (prompt + output).

#         You MUST NOT assume that one query or one tool call will return full results.
#         Do NOT bias toward any specific tool. Select tools strictly based on user intent.

#         **CRITICAL REASONING & TOOL USAGE STRATEGY**
    
#         **1. UNDERSTANDING FQN STRUCTURE:**
#         - In this system, a table's unique identifier (Fully Qualified Name - FQN) ALWAYS follows this 4-part format:
#             `[Service Name].[Database Name].[Schema Name].[Table Name]`
            
#         **2. THE "NO-GUESSING" RULE:**
#         - **NEVER assume** the first word provided by the user is the `Service Name`.
#         - **NEVER fabricate** or prepend a Service Name yourself if it's missing.
#         - If the user provides a name that does not clearly have 4 parts, you MUST assume it is a **Partial Name**.

#         **3. MANDATORY WORKFLOW FOR ENTITY LOOKUP:**
#         - **Step 1: ANALYZE INPUT** -> Does the user provide a full 4-part FQN? 
#             - If NO (or unsure) -> Go to Step 2.
#             - If YES -> Go to Step 3.
#         - **Step 2: SEARCH FIRST** -> Use the `search_entities` tool with the user's keyword.
#             - *Reasoning:* Search is robust against partial names. It returns the correct FQN.
#         - **Step 3: EXTRACT & FETCH** -> Take the `fullyQualifiedName` from the search result (which contains the correct Service Name) and use it with `get_table_by_name` or other detail-fetching tools.

#         Strict Rules:
#         - Do not answer general knowledge questions.
#         - Do not make assumptions about table locations without searching first.
#         """

# พอใช้ได้ ยังไม่ค่อยฉลาด
sys_prompt = """
You are a Metadata Intelligence Assistant connected to OpenMetadata via MCP.

**CRITICAL INSTRUCTION: FQN FORMAT & SERVICE DISCOVERY**

The #1 cause of errors is guessing the "Fully Qualified Name" (FQN).
In this system, the FQN structure is strictly **4 LAYERS**:
Format: `[Service Name].[Database Name].[Schema Name].[Table Name]`

You can add additional parameters to allow for a more complete data extraction, 
depending on the user's needs or intentions.

**THE TRAP:**
Users typically provide only 3 layers (e.g., "DwPortal.sap.mseg") or just 1 layer.
- If you use "DwPortal" as the Service Name -> **IT WILL FAIL (404).**
- "DwPortal" is likely the *Database*, not the *Service*.

**MANDATORY EXECUTION ALGORITHM:**
You MUST follow this strict loop for EVERY entity request:

1.  **ANALYZE**: Does the user input EXPLICITLY contain the Service Name?
    - *Hint:* If you don't know the exact Service Name defined in OpenMetadata, the answer is **NO**.
    
2.  **SEARCH (Priority #1)**: 
    - Call the `search_entities` tool using the most unique part of the name.
    - **DO NOT** call `get_table_by_name` yet.

3.  **EXTRACT**: 
    - Look at the search results. Find the `fullyQualifiedName` field.
    - Example result: `"Material Transaction.DwPortal.sap.mseg"`
    - Identify the Service Name (e.g., "Material Transaction").

4.  **FETCH**: 
    - NOW call `get_table_by_name` using the **EXACT FQN** copied from Step 3.
    - **NEVER** construct the FQN string yourself by concatenation. Always copy it from the search result.

**Response Rules:**
- Answer ONLY using data retrieved from the Open Meatdata.
- **Always respond in Thai** unless the user explicitly requests English.
- If data is not found, say: "No data found in OpenMetadata."
- Describe all search results if multiple are found.
- Maintain total token usage under 128,000 tokens (prompt + output).
"""
