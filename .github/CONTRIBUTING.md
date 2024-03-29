# Welcome contributor 👋

Contributions of all sorts are welcome, whether it's raising an idea for improvements,
reporting a bug, helping in reviewing open pull requests, or generally raising an issue.

When contributing please keep this in mind:

- Use issues to report bugs.
- Use discussions to raise ideas and propose features.
- Write code consistent with the project style and make sure tests and static type
  checks are passing, and that 100% test coverage is maintained.

The [README][readme] contains instructions for getting started with development.

[readme]: https://github.com/aiven/kio/blob/main/README.md#development

We use [squash merging] to achieve a linear git history. This means every PR needs to be
a logic unit of changes to the code-base, that makes sense to be squashed. This also
allows for pushing many "fix" commits to feature branches without using force push.

[squash merging]:
  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges#squash-and-merge-your-commits

## Releases

Releases of the project follow [Semantic Versioning v2.0.0][semver]. To publish a new
release, after merging an updated `__version__` property, just create a release in the
Github UI and publish it, making sure to use an identical version as the property, and
to choose to create a tag on publish. A Github Actions workflow will then publish the
library to PyPI.

[semver]: https://semver.org/spec/v2.0.0.html
