# Generated Dockerfiles
This directory contains Dockerfiles generated with the assistance of large language models (LLMs) to create intentionally vulnerable containerized environments for cyber range applications.


The folder is organized in two main subfolders:

- **ModelSelection**: contains Dockerfiles generated during the Model Selection phase (ChatGPT, Bing, Gemini).
- **BestModelAnalysis**: contains Dockerfiles generated during the Best Model Analysis phase (GPT-3.5). This folder is further organized as follows:
  
	- **LinuxServices**: Dockerfiles for vulnerable Linux software and services.
		- **Fixed**: Human-created fixed versions for each CVE, with subfolders for each vulnerability (e.g., `CVE-2012-2122_generic`, `CVE-2012-2122_source`). These may include additional configuration files as needed.
		- **LLM**: LLM-generated Dockerfiles for the same set of vulnerabilities, organized similarly to the Fixed folder.
  
	- **WebApps**: Dockerfiles for vulnerable web applications.
		- **Fixed**: Human-created fixed versions, organized by application (e.g., `custom`, `drupal`, `joomla`, `wordpress`). Each application folder contains subfolders for each CVE and deployment type (e.g., `CVE-2018-10504_compose`, `CVE-2018-10504_single`).
		- **LLM**: LLM-generated Dockerfiles, organized in the same way as the Fixed folder.
		- **WordPress**: Contains a detailed breakdown for CVE-2015-5180, including Check, HumanFix, and LLM subfolders, each with `compose` and `single` deployment types.

Below is a partial tree of the BestModelAnalysis directory for reference:

```
BestModelAnalysis
├── LinuxServices
│   ├── Fixed
│   │   ├── CVE-2012-2122_generic
│   │   │   └── Dockerfile
│   │   ├── ...
│   └── LLM
│       ├── CVE-2012-2122_generic
│       │   └── Dockerfile
│       ├── ...
└── WebApps
		├── Fixed
		│   ├── custom
		│   │   ├── CVE-2013-0177_compose
		│   │   │   └── Dockerfile
		│   │   ├── ...
		│   ├── drupal
		│   │   ├── CVE-2018-7600_compose
		│   │   │   ├── docker-compose.yml
		│   │   │   └── Dockerfile
		│   │   ├── ...
		│   ├── joomla
		│   │   ├── ...
		│   └── wordpress
		│       ├── CVE-2018-10504_compose
		│       │   ├── docker-compose.yml
		│       │   └── Dockerfile
		│       ├── ...
		├── LLM
		│   ├── custom
		│   │   ├── ...
		│   ├── drupal
		│   │   ├── ...
		│   ├── joomla
		│   │   ├── ...
		│   └── wordpress
		│       ├── ...
		└── WordPress
				└── CVE-2015-5180
						├── Check
						│   └── Dockerfile
						├── HumanFix
						│   ├── compose
						│   │   ├── docker-compose.yml
						│   │   └── Dockerfile
						│   └── single
						│       └── Dockerfile
						├── LLM
						│   ├── compose
						│   │   ├── docker-compose.yml
						│   │   └── Dockerfile
						│   └── single
						│       └── Dockerfile
						└── README.md
```



