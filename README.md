Compile c code to a.out
`python pytest.py` should be identical to running './a.out' when passing test cases in
`python runtest.py a b c` (*a*,*b*,*c* are any numbers) will compare ./a.out's output to pytest's and display any differences. It will run every test case up to a buffer size of a, up to b producers/consumers, and up to c loop iterations.
For example, try `python pytest.py < test_1.txt` or `python runtest.py 5 5 5`.
Run `pip install tqdm` to have a progress bar. 
