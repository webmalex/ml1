from builtins import print


def t1():
    import numpy as np
    X = np.random.normal(loc=1, scale=10, size=(1000, 50))
    print(X)

    m = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    X_norm = ((X - m) / std)
    print(X_norm)

    Z = np.array([[4, 5, 0],
                  [1, 9, 3],
                  [5, 1, 1],
                  [3, 3, 3],
                  [9, 9, 9],
                  [4, 7, 1]])
    r = np.sum(Z, axis=1)
    print(np.nonzero(r > 10))

    A = np.eye(3)
    B = np.eye(3)
    print(A)
    print(B)

    AB = np.vstack((A, B))
    print(AB)


def pf(name, value):
    f = open(name + '.txt', 'w')
    f.write(str(value))
    f.close()
    print(name + '="%s"\n' % value)


def lesson1():
    import pandas
    data = pandas.read_csv('train.csv', index_col='PassengerId')

    def q1_1():
        d = data['Sex'].value_counts()
        pf('1_1', '%s %s' % (d[0], d[1]))
        print(d, '\n')

    def q1_2():
        d = data['Survived'].value_counts()
        r = round(d[1] / d.sum() * 100, 2)
        pf('1_2', r)
        print(d, '\n')

    def q1_3():
        d = data['Pclass'].value_counts()
        r = round(d[1] / d.sum() * 100, 2)
        pf('1_3', r)
        print(d, '\n')

    def q1_4():
        d = data['Age']
        a = round(d.sum() / d.count(), 2)
        m = d.median()
        pf('1_4', '%s %s' % (a, m))

    def q1_5():
        d = round(data['SibSp'].corr(data['Parch']), 2)
        pf('1_5', d)

    q1_1()
    q1_2()
    q1_3()
    q1_4()
    q1_5()


def lesson2():
    def t1():
        from sklearn.datasets import load_iris
        from sklearn import tree
        iris = load_iris()
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(iris.data, iris.target)
        # from sklearn.externals.six import StringIO
        with open("iris.dot", 'w') as f:
            f = tree.export_graphviz(clf, out_file=f)

        # brew install graphviz
        from os import system
        system("dot -Tpdf iris.dot -o iris.pdf")
        # from subprocess import call
        # call(["dot", "-Tpdf", "iris.dot", "-o", "iris.pdf"])

    def t2():
        import numpy as np
        from sklearn.tree import DecisionTreeClassifier
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 1, 0])
        clf = DecisionTreeClassifier()
        clf.fit(X, y)
        importances = clf.feature_importances_
        print(importances)

    def t3():
        import pandas
        df = pandas.read_csv('train.csv', index_col='PassengerId')
        d = df[['Pclass', 'Fare', 'Age', 'Sex', 'Survived']].dropna().replace('male', 1).replace('female', 0)
        # print(d1)
        from sklearn.tree import DecisionTreeClassifier
        clf = DecisionTreeClassifier()
        clf.random_state = 241
        clf.fit(d[['Pclass', 'Fare', 'Age', 'Sex']], d['Survived'])
        importances = clf.feature_importances_
        print(importances)
        # [ 0.13700004  0.31259037  0.24989737  0.30051221]
        # [ 0.14000522  0.30343647  0.2560461   0.30051221]
        pf('2', 'Fare Sex')


    t3()

def lesson3():
    def t1():
        X = [[0], [1], [2], [3]]
        y = [0, 0, 1, 1]
        from sklearn.neighbors import KNeighborsClassifier
        neigh = KNeighborsClassifier(n_neighbors=3)
        neigh.fit(X, y)
        KNeighborsClassifier(...)
        print(neigh.predict([[1.1]]))
        print(neigh.predict_proba([[0.9]]))


    def t2():
        import numpy as np
        from sklearn.cross_validation import KFold
        X = np.array([[1, 2], [3, 4], [1, 2], [3, 4]])
        y = np.array([1, 2, 3, 4])
        kf = KFold(4, n_folds=2)
        print(kf)
        for train_index, test_index in kf:
            print("TRAIN:", train_index, "TEST:", test_index)
            # X_train, X_test = X[train_index], X[test_index]
            # y_train, y_test = y[train_index], y[test_index]


    def t3():

        def a(x, y):

            # 1.3
            from sklearn import cross_validation
            kf = cross_validation.KFold(len(y), n_folds=5, shuffle=True, random_state=42)
            # print(kf)

            # 1.4
            # from sklearn import svm
            # clf = svm.SVC(kernel='linear', C=1)
            from sklearn.neighbors import KNeighborsClassifier
            def test(i):
                clf = KNeighborsClassifier(n_neighbors=i)
                scores = cross_validation.cross_val_score(clf, x, y, cv=kf)
                score = sum(scores) / len(scores)
                # print(i, score, scores)
                return score
            l = list(map(test, range(1, 51)))
            m = max(l)
            return l.index(m) + 1, round(m, 2)

        # 1.1
        import pandas
        d = pandas.read_csv('wine.data.txt', header=None)

        # 1.2
        y = d[0]
        x = d.drop([0], axis=1)

        # 1.4
        i, m = a(x, y)
        pf('3_1', i)
        pf('3_2', m)

        # 1.5
        from sklearn.preprocessing import scale
        xs = scale(x)
        i, m = a(xs, y)
        pf('3_3', i)
        pf('3_4', m)
        # print(xs)

    t3()

def lesson4():
    def t1():
        # 1
        # import sklearn
        import numpy
        from sklearn.datasets import load_boston
        d = load_boston()
        xr = d.data
        y = d.target
        # print(y, x)

        # 2
        from sklearn.preprocessing import scale
        x = scale(xr)

        # 3
        from sklearn import cross_validation, neighbors
        kf = cross_validation.KFold(len(y), n_folds=5, shuffle=True, random_state=42)
        def test(p):
            clf = neighbors.KNeighborsRegressor(n_neighbors=5, weights='distance', metric='minkowski', p=p)
            scores = cross_validation.cross_val_score(clf, x, y, cv=kf, scoring='mean_squared_error')
            score = sum(scores) / len(scores)
            # print(p, score, scores)
            return score
        from numpy import linspace
        ap = linspace(1, 10, num=200)
        # print(ap)
        l = list(map(test, ap))
        m = max(l)
        pf('4', round(ap[l.index(m)], 1))
        print(m, l)
        # return l.index(m) + 1, round(m, 2)

    t1()


def lesson5():
    import numpy as np
    def t1():
        from sklearn.linear_model import Perceptron
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 1, 0])
        clf = Perceptron()
        clf.fit(X, y)
        predictions = clf.predict(X)
        print(predictions)

    def t2():
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_train = np.array([[100.0, 2.0], [50.0, 4.0], [70.0, 6.0]])
        X_test = np.array([[90.0, 1], [40.0, 3], [60.0, 4]])
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        print(X_train_scaled)
        print(X_test_scaled)

    def t():
        # 1
        from pandas import read_csv
        df = read_csv('perceptron-train.csv', header=None)
        dt = read_csv('perceptron-test.csv', header=None)
        print(df, dt)

    t()

lesson5()
