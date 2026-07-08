# Lab APS Documentation

This directory contains the architecture, requirements, implementation guidance, and development notes for the Laboratory Advanced Planning & Scheduling Platform.

## Documentation Map

### 1. Project Foundation

- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — project purpose, architecture freeze, and current working rules.
- [ARCHITECTURE_INDEX.md](ARCHITECTURE_INDEX.md) — high-level index of all architecture documents.
- [ARCHITECTURE_LOG.md](ARCHITECTURE_LOG.md) — current milestone and progress snapshot.

### 2. Requirements and Vision

- [01_Vision/01_Vision.md](01_Vision/01_Vision.md) — product vision and goals.
- [01_Vision/02_Terminology.md](01_Vision/02_Terminology.md) — domain terminology.
- [02_SRS/01_Introduction.md](02_SRS/01_Introduction.md) — requirements baseline.
- [02_SRS/02_Business_Background.md](02_SRS/02_Business_Background.md) — business context.
- [02_SRS/03_Business_Process.md](02_SRS/03_Business_Process.md) — key workflows.
- [02_SRS/04_Functional_Requirements.md](02_SRS/04_Functional_Requirements.md) — functional requirement catalog.
- [02_SRS/05_Business_Object_Model.md](02_SRS/05_Business_Object_Model.md) — domain object model.

### 3. Architecture Design

- [03_SAD/01_Bussiness_Capability.md](03_SAD/01_Bussiness_Capability.md) — business capability map.
- [03_SAD/02_System_Architecture.md](03_SAD/02_System_Architecture.md) — system architecture.
- [03_SAD/03_Domain_Architecture.md](03_SAD/03_Domain_Architecture.md) — domain architecture.
- [03_SAD/04_Plan_Aggregate.md](03_SAD/04_Plan_Aggregate.md) — aggregate design.
- [03_SAD/05_Scheduling_Architecture.md](03_SAD/05_Scheduling_Architecture.md) — scheduling architecture.
- [03_SAD/06_Application_Architecture.md](03_SAD/06_Application_Architecture.md) — application-layer design.
- [03_SAD/07_Database_Conceptual_Model.md](03_SAD/07_Database_Conceptual_Model.md) — conceptual data model.
- [03_SAD/08_Plan_Lifecycle.md](03_SAD/08_Plan_Lifecycle.md) — lifecycle model.
- [03_SAD/09_Plan_Version_Architecture.md](03_SAD/09_Plan_Version_Architecture.md) — versioning model.
- [03_SAD/10_Persistence_Architecture.md](03_SAD/10_Persistence_Architecture.md) — persistence architecture.
- [03_SAD/11_Conceptual_ERD.md](03_SAD/11_Conceptual_ERD.md) — conceptual ERD.
- [03_SAD/12_Physical_Database_Design.md](03_SAD/12_Physical_Database_Design.md) — physical DB design.
- [03_SAD/13_Architecture_Constraints.md](03_SAD/13_Architecture_Constraints.md) — architecture constraints.
- [03_SAD/14_Solver_Model.md](03_SAD/14_Solver_Model.md) — solver and optimization design.
- [03_SAD/15_Module_Interaction.md](03_SAD/15_Module_Interaction.md) — module interactions.
- [03_SAD/16_API_Architecture.md](03_SAD/16_API_Architecture.md) — API architecture.
- [03_SAD/17_Deployment_Architecture.md](03_SAD/17_Deployment_Architecture.md) — deployment architecture.
- [03_SAD/18_Coding_Guidelines.md](03_SAD/18_Coding_Guidelines.md) — coding guidelines.
- [03_SAD/19_Project_Structure.md](03_SAD/19_Project_Structure.md) — project structure guidance.
- [03_SAD/20_Development_Workflow.md](03_SAD/20_Development_Workflow.md) — development workflow.
- [03_SAD/Architecture_Update_2026-07_Vue3.md](03_SAD/Architecture_Update_2026-07_Vue3.md) — frontend architecture upgrade note.

### 4. Design Decisions

- [04_ADR/ADR-001-Plan-Aggregate-Root.md](04_ADR/ADR-001-Plan-Aggregate-Root.md) — plan as aggregate root.
- [04_ADR/ADR-002-Plan-Version-Instead-of-Planning-Session.md](04_ADR/ADR-002-Plan-Version-Instead-of-Planning-Session.md) — plan versioning decision.
- [04_ADR/ADR-003-Workflow-Definition-and-Workflow-Instance.md](04_ADR/ADR-003-Workflow-Definition-and-Workflow-Instance.md) — workflow modeling decision.
- [04_ADR/ADR-004-Operation-Definition-and-Operation-Instance.md](04_ADR/ADR-004-Operation-Definition-and-Operation-Instance.md) — operation modeling decision.
- [04_ADR/ADR-005-Scheduling-Model-as-an-Anti-Corruption-Layer.md](04_ADR/ADR-005-Scheduling-Model-as-an-Anti-Corruption-Layer.md) — scheduling model separation.
- [04_ADR/ADR-006-Constraint-Model-Instead-of-Direct-Solver-Constraints.md](04_ADR/ADR-006-Constraint-Model-Instead-of-Direct-Solver-Constraints.md) — constraint model decision.
- [04_ADR/ADR-007-Separate-Constraint-Model-and-Objective-Model.md](04_ADR/ADR-007-Separate-Constraint-Model-and-Objective-Model.md) — objective and constraint split.
- [04_ADR/ADR-008-Planning-Context-Uses-Snapshots.md](04_ADR/ADR-008-Planning-Context-Uses-Snapshots.md) — planning context snapshot decision.
- [04_ADR/ADR-009-Reject-Direct-Database-Driven-Scheduling.md](04_ADR/ADR-009-Reject-Direct-Database-Driven-Scheduling.md) — scheduling isolation decision.
- [04_ADR/ADR-010-Separate-Laboratory-Definition-and-Planning-Domains.md](04_ADR/ADR-010-Separate-Laboratory-Definition-and-Planning-Domains.md) — domain separation decision.
- [04_ADR/ADR-011-Adopt-Vue3-SPA-Frontend.md](04_ADR/ADR-011-Adopt-Vue3-SPA-Frontend.md) — frontend architecture decision.

### 5. Planning and Constraint Models

- [05_Constraint_Framework/01_Constraint_Framework.md](05_Constraint_Framework/01_Constraint_Framework.md) — constraint architecture.
- [05_Constraint_Framework/02_Constraint_Mapping.md](05_Constraint_Framework/02_Constraint_Mapping.md) — mapping rules.
- [05_Constraint_Framework/03_Constraint_Specification.md](05_Constraint_Framework/03_Constraint_Specification.md) — constraint specifications.
- [06_Planning_Model/01_Planning_Model.md](06_Planning_Model/01_Planning_Model.md) — planning model overview.
- [06_Planning_Model/02_Scheduling_Model.md](06_Planning_Model/02_Scheduling_Model.md) — scheduling model.
- [06_Planning_Model/03_Planning_Problem.md](06_Planning_Model/03_Planning_Problem.md) — planning problem representation.

### 6. Data, API, UI, and State

- [07_Database/01_Canonical_Data_Model.md](07_Database/01_Canonical_Data_Model.md) — canonical data model.
- [07_Database/02_Canonical_Object_Specification.md](07_Database/02_Canonical_Object_Specification.md) — canonical object spec.
- [07_Database/03_Physical_ERD.md](07_Database/03_Physical_ERD.md) — physical ERD.
- [07_Database/04_Table_Dictionary.md](07_Database/04_Table_Dictionary.md) — table dictionary.
- [07_Database/05_SQLAlchemy_Mapping_Guide.md](07_Database/05_SQLAlchemy_Mapping_Guide.md) — ORM mapping guidance.
- [08_API/01_API_Resource_Model.md](08_API/01_API_Resource_Model.md) — API resource model.
- [08_API/02_Planning_API.md](08_API/02_Planning_API.md) — planning API.
- [08_API/03_Resource_API.md](08_API/03_Resource_API.md) — resource API.
- [08_API/04_API_Response_Standard.md](08_API/04_API_Response_Standard.md) — API response standard.
- [09_UI/01_Information_Architecture.md](09_UI/01_Information_Architecture.md) — UI information architecture.
- [09_UI/02_Navigation_Model.md](09_UI/02_Navigation_Model.md) — UI navigation model.
- [09_UI/03_User_Flow.md](09_UI/03_User_Flow.md) — user flows.
- [09_UI/04_Plan_Workspace_Design.md](09_UI/04_Plan_Workspace_Design.md) — plan workspace UI design.
- [09_UI/05_Plan_Workspace_Wireframe.md](09_UI/05_Plan_Workspace_Wireframe.md) — workspace wireframe.
- [09_UI/06_Interaction_Specification.md](09_UI/06_Interaction_Specification.md) — interaction specification.
- [10_State_Model/01_State_Model_Overview.md](10_State_Model/01_State_Model_Overview.md) — state machine overview.
- [10_State_Model/02_Plan_State.md](10_State_Model/02_Plan_State.md) — plan state model.
- [10_State_Model/03_PlanVersion_State.md](10_State_Model/03_PlanVersion_State.md) — plan version state.
- [10_State_Model/04_Assignment_State.md](10_State_Model/04_Assignment_State.md) — assignment state.
- [10_State_Model/05_Execution_State.md](10_State_Model/05_Execution_State.md) — execution state.
- [10_State_Model/06_State_Transition_Rules.md](10_State_Model/06_State_Transition_Rules.md) — transition rules.
- [10_State_Model/07_Equipment_State.md](10_State_Model/07_Equipment_State.md) — equipment state.
- [10_State_Model/08_Staff_State.md](10_State_Model/08_Staff_State.md) — staff state.

### 7. Implementation and Delivery

- [11_Development/00_Engineering_Baseline.md](11_Development/00_Engineering_Baseline.md) — engineering baseline.
- [11_Development/00_Project_Bootstrap_Plan.md](11_Development/00_Project_Bootstrap_Plan.md) — bootstrap plan.
- [11_Development/01_Project_Architecture.md](11_Development/01_Project_Architecture.md) — implementation architecture.
- [11_Development/02_Project_Structure_Implementation.md](11_Development/02_Project_Structure_Implementation.md) — implementation structure.
- [11_Development/03_Dependency_Injection_Strategy.md](11_Development/03_Dependency_Injection_Strategy.md) — DI strategy.
- [11_Development/04_UseCase_Template.md](11_Development/04_UseCase_Template.md) — use case template.
- [11_Development/05_Repository_and_Query_Guide.md](11_Development/05_Repository_and_Query_Guide.md) — repository guidance.
- [11_Development/06_Engine_Template.md](11_Development/06_Engine_Template.md) — engine template.
- [11_Development/07_Solver_Template.md](11_Development/07_Solver_Template.md) — solver template.
- [11_Development/08_Domain_Entity_Template.md](11_Development/08_Domain_Entity_Template.md) — domain entity template.
- [11_Development/09_Testing_Template.md](11_Development/09_Testing_Template.md) — testing template.
- [11_Development/Developer_Onboarding.md](11_Development/Developer_Onboarding.md) — contributor onboarding guide.
- [11_Development/Testing_and_Validation_Guide.md](11_Development/Testing_and_Validation_Guide.md) — testing and validation guidance.
- [11_Development/Deployment_and_Operations_Guide.md](11_Development/Deployment_and_Operations_Guide.md) — deployment and operations guidance.
- [12_Development_Log/M1.1_Project_Bootstrap.md](12_Development_Log/M1.1_Project_Bootstrap.md) — M1.1 project bootstrap.
- [12_Development_Log/M1.2_Backend_Framework.md](12_Development_Log/M1.2_Backend_Framework.md) — M1.2 backend framework.
- [12_Development_Log/M1.3_Developer_CLI_Generators.md](12_Development_Log/M1.3_Developer_CLI_Generators.md) — M1.3 developer CLI code generators.
- [12_Development_Log/M2.1_Infrastructure.md](12_Development_Log/M2.1_Infrastructure.md) — M2.1 infrastructure.
- [12_Development_Log/M3.1_Planning_Domain.md](12_Development_Log/M3.1_Planning_Domain.md) — M3.1 planning domain.
- [12_Development_Log/M3.2_Plan_Version_Lifecycle.md](12_Development_Log/M3.2_Plan_Version_Lifecycle.md) — M3.2 plan version lifecycle.
- [12_Development_Log/M4.1_Scheduling_Engine.md](12_Development_Log/M4.1_Scheduling_Engine.md) — M4.1 scheduling engine.
- [12_Development_Log/M4.2_Schedule_From_Workflow.md](12_Development_Log/M4.2_Schedule_From_Workflow.md) — M4.2 schedule from persisted laboratory data.
- [12_Development_Log/M4.3_Skill_Constraint.md](12_Development_Log/M4.3_Skill_Constraint.md) — M4.3 skill constraint (multi-resource assignment).
- [12_Development_Log/M4.4_Persist_Assignments.md](12_Development_Log/M4.4_Persist_Assignments.md) — M4.4 persist assignments.
- [12_Development_Log/M5.1_Laboratory_Equipment.md](12_Development_Log/M5.1_Laboratory_Equipment.md) — M5.1 laboratory equipment.
- [12_Development_Log/M5.2_Staff_and_Workflow_Definition.md](12_Development_Log/M5.2_Staff_and_Workflow_Definition.md) — M5.2 staff and workflow definition.
- [12_Development_Log/M6.1_Frontend_Plans_View.md](12_Development_Log/M6.1_Frontend_Plans_View.md) — M6.1 frontend plans view.
- [12_Development_Log/M6.2_Frontend_Laboratory_Views.md](12_Development_Log/M6.2_Frontend_Laboratory_Views.md) — M6.2 frontend laboratory views.
- [12_Development_Log/M6.3_Frontend_Dashboard_View.md](12_Development_Log/M6.3_Frontend_Dashboard_View.md) — M6.3 frontend dashboard view.
- [12_Development_Log/M8.1_Reporting_Dashboard.md](12_Development_Log/M8.1_Reporting_Dashboard.md) — M8.1 reporting dashboard.
- [12_Development_Log/M9.1_Execution_Assignment_Lifecycle.md](12_Development_Log/M9.1_Execution_Assignment_Lifecycle.md) — M9.1 execution assignment lifecycle.
- [12_Development_Log/M7.1_API_Response_Envelope.md](12_Development_Log/M7.1_API_Response_Envelope.md) — M7.1 API response envelope.
- [12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md](12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md) — session index across milestones.
- [12_Development_Log/Documentation_Improvement_Plan.md](12_Development_Log/Documentation_Improvement_Plan.md) — current documentation improvement plan.

## Recommended Reading Order

If you are new to the project, read the documents in this order:

1. [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)
2. [01_Vision/01_Vision.md](01_Vision/01_Vision.md)
3. [02_SRS/01_Introduction.md](02_SRS/01_Introduction.md)
4. [03_SAD/02_System_Architecture.md](03_SAD/02_System_Architecture.md)
5. [11_Development/00_Engineering_Baseline.md](11_Development/00_Engineering_Baseline.md)
6. [07_Database/03_Physical_ERD.md](07_Database/03_Physical_ERD.md)
7. [08_API/02_Planning_API.md](08_API/02_Planning_API.md)

## Documentation Status Notes

The project documentation is currently divided into three maturity levels:

- Baseline and frozen: architecture, requirements, and major design decisions.
- Draft or implementation-ready design: API, UI, database, and planning models.
- Pending implementation follow-up: local onboarding, testing workflow, and deployment runbook.

## Contribution Guideline

When changing the system, update the related documents together with the code:

- business rules change → update requirements and relevant architecture docs
- domain model change → update SAD, state model, and database docs
- API change → update API docs and related UI docs
- solver or planning logic change → update planning model and constraint docs
