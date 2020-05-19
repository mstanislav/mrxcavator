# DSU CSC-842 - mrxcavator

mrxcavator is a CLI implementation for [CRXCavator](https://crxcavator.io) being built as part of DSU's CSC-842, "Security Tool Development"

The following overview was taken from the project's [about](https://crxcavator.io/docs#/README) page:
> CRXcavator automatically scans the entire Chrome Web Store every 3 hours and produces a quantified risk score for each Chrome Extension based on several factors. These factors include permissions, inclusion of vulnerable third party javascript libraries, weak content security policies, missing details from the Chrome Web Store description, and more. Organizations can use this tool to assess the Chrome Extensions they have installed and to move towards implementing explicit allow (whitelisting) for their organization.

The development of this tool will have five "releases" that related to the course's submission deadlines. As tool releases are produced, this README.md will be updated to share some highlights of what was contributed during that release.

1. Release #1 - 05/24
2. Release #2 - 06/07
3. Release #3 - 06/21
4. Release #4 - 07/05
5. Release #5 - 07/19

In general, the tool hopes to provide an easy-to-use interface to submit extensions to CRXcavator, gather results, cache results, provide basic reporting, and likely leverage some CLI-visualization libraries to improve user experience. At this time, no public CLI tool exists for this service, so I feel that the contribution to the community is a good focus of effort.
