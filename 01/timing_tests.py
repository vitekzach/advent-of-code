import timeit

REPEAT_TIMES = 100000

t = timeit.Timer(
    'get_final_sum(["1abc2", "pqr3stu8vwx","a1b2c3d4e5f","treb7uchet",])', setup="from functions import get_final_sum"
)
elapsed = t.timeit(number=REPEAT_TIMES)
print(f"Get all digits {REPEAT_TIMES}x: {elapsed}s.")

t_crawl = timeit.Timer(
    'get_final_sum(["1abc2", "pqr3stu8vwx","a1b2c3d4e5f","treb7uchet",])', setup="from functions import get_final_sum"
)
elapsed_crawl = t_crawl.timeit(number=REPEAT_TIMES)
print(f"Get all digits with crawl {REPEAT_TIMES}x: {elapsed_crawl}s.")
