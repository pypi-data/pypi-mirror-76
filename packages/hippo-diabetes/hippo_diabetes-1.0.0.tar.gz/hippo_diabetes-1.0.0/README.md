# Details of this Folder

This is where the bulk of the Python code lives that does the modeling. This is what executes in the pipeline after [all of the data is processed](data/interim).

Each subfolder here is a separate module serving a specific purpose:

| Module Name            | Purpose                                                                |
|-------------           |-----------------------                                                 |
| [Raven](./raven)       | Getting Data                                                           |
| [Egret](./egret)       | Data Cleaning                                                          |
| [Otter](./otter)       | Building Care Gaps                                                     |
| [Hippo](./hippo)       | Core Model-Building                                                    |
| [Moose](./moose)       | Analytics and Outputs                                                  |
| [Rhino](./rhino)       | [CPL](https://cpl-json-ui-oci-dev.aetapps-dev.aetna.com/) Integrations |
| [Whale](./whale)       | Unit Testing                                                           |
