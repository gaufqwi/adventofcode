def main(data, part, log):
    score = 0
    openers = partners.keys()
    complete_scores = []
    for i, line in enumerate(data):
        expect = []
        ok = True
        for c in line.strip():
            if c in openers:
                expect.append(partners[c])
            else:
                if c != expect[-1]:
                    score += values[c]
                    ok = False
                    break
                else:
                    expect.pop()
        if ok:
            expect.reverse()
            complete_score = 0
            for c in expect:
                complete_score = 5 * complete_score + completion_values[c]
            complete_scores.append(complete_score)

    if part == 1:
        print(f'Total score is {score}')
    else:
        complete_scores.sort()
        print(f'Middle complete score is {complete_scores[len(complete_scores) // 2]}')

values = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

completion_values = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

partners = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
