# Architecture and framework authority

Paperclip owns goals, roles and budgets. OpenClaw is the operator gateway. LangGraph is the sole durable execution state machine. CrewAI specialist teams and LangChain adapters operate inside bounded stages. NVIDIA NIM is an inference contract. GraphRAG retrieves only the dependency subgraph needed for the current change.

The implemented engine is deterministic and provider-neutral. Framework, NVIDIA, cloud, Terraform/OpenTofu, Ansible and Chef integrations remain contracts until exercised.

