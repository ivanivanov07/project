import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns

with st.echo(code_location='below'):
    st.title("How girls and boys perform on exams?")
    st.write('Давайте узнаем насколько успешно представители обоих полов сдают экзамены.\n От чего же зависит успех?\n\n\n\n\n\n\n\n\n ')
    st.write('Для начала давайте просто узнаем сколько человек каждого пола участвовали в нашем эксперименте.\n Здесь вы можете видеть классическую круговую диаграмму.')

    def binarize(data, label):
        temp = {}
        i = 1
        for el in data[label]:
            if el not in temp:
                temp[el] = i
                temp[i] = 'trash'
                i += 1
                data[label].replace(el, temp[el], inplace=True)

    @st.cache
    def get_data():
            data_url = ("StudentsPerformance.csv")
            df = pd.read_csv(data_url)
            df['average score'] = (df['writing score'] + df['reading score'] + df['math score']) / 3
            df['average score without math'] = (df['writing score'] + df['reading score']) / 2
            df['average score without reading'] = (df['writing score'] + df['math score']) / 2
            df['average score without writing'] = (df['math score'] + df['reading score']) / 2
            # binarize(df, 'parental level of education')
            # binarize(df, 'lunch')
            return df


    df = get_data()
    fig, ax1 = plt.subplots()
    colors = ['#d16996', '#beb6dd']
    sizes = [len(df[df['gender'] == 'female']), len(df[df['gender'] == 'male'])]
    ax1.pie(sizes, labels=['Female', 'Male'], autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color':"white"})
    fig.set_facecolor('#101414')
    st.title('Distribution of genders')
    st.pyplot(fig)
    st.write('Сейчас давайте посмотрим как выглядят баллы по каждому экзамену у девочек и мальчиков. Это поможет нам представить, кто показывает более высокие результаты.')
    st.write('Выберите какой экзамен хотите посмотреть.')
    choice = st.radio('Choose:', ['Math score distribution between girls and boys',
                                  'Reading score distribution between girls and boys',
                                  'Writing score distribution between girls and boys'])

    if choice == 'Math score distribution between girls and boys':
        hist_data = [df[df['gender'] == 'female']['math score'], df[df['gender'] == 'male']['math score']]
        group_labels = ['Female', 'Male']
        fig = ff.create_distplot(
                 hist_data, group_labels, bin_size=[.1, .25, .5], colors=colors)
        st.title('Math score distribution between girls and boys')
        st.plotly_chart(fig, use_container_width=True)

    elif choice == 'Reading score distribution between girls and boys':
        hist_data = [df[df['gender'] == 'female']['reading score'], df[df['gender'] == 'male']['reading score']]
        group_labels = ['Female', 'Male']
        fig = ff.create_distplot(
                 hist_data, group_labels, bin_size=[.1, .25, .5], colors=colors)
        st.title('Reading score distribution between girls and boys')
        st.plotly_chart(fig, use_container_width=True)

    elif choice == 'Writing score distribution between girls and boys':
        hist_data = [df[df['gender'] == 'female']['writing score'], df[df['gender'] == 'male']['writing score']]
        group_labels = ['Female', 'Male']
        fig = ff.create_distplot(
                 hist_data, group_labels, bin_size=[.1, .25, .5], colors=colors)
        st.title('Writing score distribution between girls and boys')
        st.plotly_chart(fig, use_container_width=True)

    st.write('Вот некие результаты: В математике чуть получше мальчики. На экзамене по reading лучше себя показывают девочки. Аналогично происходит и на writing тесте - девочки видимо пишут более проникновенные сочинения.')
    st.title('Score linear regression')
    st.write('Теперь обратимся к регрессии. Итак, давайте смотреть как связаны результаты экзамена по любому предмету и средней балл за два других экзамена (не считая конкретный, конечно же). ')
    st.write('Выберите какой экзамен вы хотите посмотреть:')
    choice = st.radio('Choose:', ['average score without math',
                                  'average score without reading',
                                  'average score without writing'])

    if choice == 'average score without math':
        sns.set_style("white")
        gridobj = sns.lmplot(x="average score without math", y="math score", data=df,
                             height=7, aspect=1.6, robust=True, palette='tab10',
                             scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))
        # Decorations
        gridobj.set(xlim=(0, 120), ylim=(0, 120))
        plt.title("Math score regression with average score without math", fontsize=20)
        plt.show()
        st.pyplot(gridobj)
    elif choice == 'average score without writing':
        sns.set_style("white")
        gridobj = sns.lmplot(x="average score without writing", y="writing score", data=df,
                             height=7, aspect=1.6, robust=True, palette='tab10',
                             scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))
        # Decorations
        gridobj.set(xlim=(0, 120), ylim=(0, 120))
        plt.title("Writing score regression with average score without writing", fontsize=20)
        plt.show()
        st.pyplot(gridobj)
    elif choice == 'average score without reading':
        sns.set_style("white")
        gridobj = sns.lmplot(x="average score without reading", y="reading score", data=df,
                             height=7, aspect=1.6, robust=True, palette='tab10',
                             scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))
        # Decorations
        gridobj.set(xlim=(0, 120), ylim=(0, 120))
        plt.title("Reading score regression with average score without reading", fontsize=20)
        plt.show()
        st.pyplot(gridobj)

    st.write('Мы видим, что чем выше балл за конкретный экзамен, тем выше средний балл за другие экзамены. Это подтверждается и эмпирически - в среднем человек, который показывает хорошие результаты в одной области науки, хорош и во многих других. Как говорится, талантливый человек талантлив во всем.')
    st.write('Теперь возьмем один из важнейших параметров успеха на экзамене - подготовку.Давайте посмотрим на распределения среднего балла подготовленных студентов и неподготовленных.Будем смотреть мальчиков или девочек?')

    # fig = plt.figure(figsize=(10, 4))
    # # ax1.scatter(df['parental level of education'], df['lunch'])
    # df_counts = df.groupby(['parental level of education', 'lunch']).size().reset_index()
    # df_counts.plot.bar(width=1, stacked=True)
    # # sns.stripplot(df_counts['parental level of education'], df_counts['lunch'])
    # plt.show()
    # st.pyplot(fig)


    x = df[(df['gender'] == 'female') & (df['test preparation course'] == 'none')]['average score']
    y = df[(df['gender'] == 'male') & (df['test preparation course'] == 'none')]['average score']
    z = df[(df['gender'] == 'female') & (df['test preparation course'] == 'completed')]['average score']
    a = df[(df['gender'] == 'male') & (df['test preparation course'] == 'completed')]['average score']

    st.title('Distribution of average score')
    choice = st.radio('Choose:', ['Distribution of average score between male with test preparation',
                                  'Distribution of average score between male without test preparation',
                                  'Distribution of average score between female with test preparation',
                                  'Distribution of average score between female without test preparation'])

    if choice == 'Distribution of average score between male with test preparation':
        fig, ax = plt.subplots()
        plt.hist(a, 50, density=True, facecolor='#407088', alpha=0.75)
        plt.title('Distribution of average score between male with test preparation')
        st.pyplot(fig)
    elif choice == 'Distribution of average score between male without test preparation':
        fig, ax = plt.subplots()
        plt.hist(y, 50, density=True, facecolor='#407088', alpha=0.75)
        plt.title('Distribution of average score between male without test preparation')
        st.pyplot(fig)
    elif choice == 'Distribution of average score between female with test preparation':
        fig, ax = plt.subplots()
        plt.hist(z, 50, density=True, facecolor='#ffb5b5', alpha=0.75)
        plt.title('Distribution of average score between female with test preparation')
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        plt.hist(x, 50, density=True, facecolor='#ffb5b5', alpha=0.75)
        plt.title('Distribution of average score between female without test preparation')
        st.pyplot(fig)

