# ModelWorks2

## How to Contribute
First go to the [Jira board](https://itaiadd.atlassian.net/jira/software/projects/MW2/boards/1){:target="_blank"} to see unassigned issues or to create a new one. Assign the issue to yourself and move the issue to 'In Progress' then follow the steps below. 

1.  Clone the repository with
    ```bash
    git clone git@github.com:ItaiAdd/ModelWorks2.git
    ```
    or

    ```bash
    git clone https://github.com/ItaiAdd/ModelWorks2.git
    ```
2.  Create a new branch named `MW2-<issue_number>-<short_description>` using
    ```bash
    git checkout -b <BRANCH-NAME>
    ```
3.  Do your thing and when you're done push to GitHub with
    ```bash
    git push -u origin <BRANCH-NAME>
    ```
4.  Create a pull request on GitHub and move the issue to 'Needs Review' on the Jira board.
</br>
</br>
</br>

## Development Principles of MW2
* ***Clean code is great, but, over abstraction is not***. If someone has to peel back 4 layers of abstraction contained in 5 different files....that code sucks.
</br>
</br>

* ***Don't shoot for a perfect solution; good enough is good enough***. We can all argue about the **best** solution after we find **a** solution.
</br>
</br>

* ***Minimise relience on anything outside of the [Python standard library](https://docs.python.org/3/library/index.html){:target="_blank"}***. If you are importing Pandas just to read a csv file then I will make a bot to spread a rumour that you put underscores in numbers. 