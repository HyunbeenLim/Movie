import numpy as np
import pandas as pd
from scipy.special import digamma, polygamma

######################## 연산을 돕는 함수 ########################

# 작은 수에 대해 안전한 로그 변환을 해주는 함수
def safe_log(vector):
    length = len(vector)
    new_vector = [0] * length

    for i in range(length):
        if vector[i] < 1e-10:
            new_vector[i] = np.log(1e-10)
        else:
            new_vector[i] = np.log(vector[i])

    return new_vector

# logsum
def logsumexp(vector):
    c = np.max(vector)
    result = c + np.log(np.sum(np.exp(vector - c)))
    return result

# psi 변환
def psi_vec(vector):
    length = len(vector)
    new_vector = [0] * length

    sum_value = sum(vector)
    di_sum = digamma(sum_value)

    for i in range(length):
        if vector[i] < 1e-10:
            new_vector[i] = digamma(1e-10) - di_sum             # smooting
        else:
            new_vector[i] = digamma(vector[i]) - di_sum
    
    return new_vector

# trigamma
def safe_tri(x):
    if x < 1e-10:
        x = polygamma(1, x)             # smoothing
    else:
        x = polygamma(1, x)
    return x

# 벡터의 모든 요소에 특정 숫자 더해주기
def vector_int_sum(vector, x):
    length = len(vector)
    new_vector = [0] * length
    for i in range(length):
        new_vector[i] = vector[i] + x
    return new_vector

# 벡터의 모든 요소에 특정 숫자 곱해주기
def vector_int_prod(vector, x):
    length = len(vector)
    new_vector = [0] * length
    for i in range(length):
        new_vector[i] = vector[i] * x
    return new_vector


# 두 벡터에서, 같은 자리에 있는 요소끼리 더해주기
def vector_sum(v1, v2):
    new_vec = [0] * len(v1)

    for i in range(len(v1)):
        new_vec[i] = v1[i] + v2[i]

    return new_vec

# 두 벡터에서, 같은 자리에 있는 요소끼리 빼주기
def vector_diff(v1, v2):
    new_vec = [0] * len(v1)

    for i in range(len(v1)):
        new_vec[i] = v1[i] - v2[i]

    return new_vec

# 두 벡터에서, 같은 자리에 있는 요소끼리 곱해주기
def vector_prod(v1, v2):
    new_vec = [0] * len(v1)

    for i in range(len(v1)):
        new_vec[i] = v1[i] * v2[i]

    return new_vec

# Lower Bound 계산
def computeLB(alpha, eta, phi, gamma, lamb, M, k, V):
    N = len(phi) // k

    gam_frac = [0] * k
    psi_gam_frac = [0] * k
    phi_gam_frac = [0] * k

    term1 = 0
    entropy_theta = 0
    phi_gam_term = 0

    for d in range(M):
        gam_frac = gamma[(d*k):((d+1)*k)]

        if all(value == 0 for value in gam_frac):
            continue
        
        psi_gam_frac = psi_vec(gam_frac)

        term1 += sum(vector_prod(vector_int_sum(alpha, -1), psi_gam_frac))
        entropy_theta += sum(vector_prod(vector_int_sum(gam_frac, -1), psi_gam_frac))

        for n in range(N):
            phi_gam_frac = phi[(n*k):((n+1)*k)]
            phi_gam_term += sum(vector_prod(phi_gam_frac, vector_diff(psi_gam_frac, safe_log(phi_gam_frac)))      )

    term2 = 0
    entropy_beta = 0

    lambda_frac = [0] * V
    psi_lam_frac = [0] * V

    for i in range(k):
        lambda_frac = lamb[(i*V):((i+1)*V)]
        psi_lam_frac = psi_vec(lambda_frac)

        term2 += sum(vector_prod(vector_int_sum(eta, -1), psi_lam_frac))
        entropy_beta += sum(vector_prod(vector_int_sum(lambda_frac, -1), psi_lam_frac))

    phi_lam_term = 0

    lambda_t = [0] * k
    psi_lam = [0] * k
    phi_lam_frac = [0] * k

    for j in range(V):
        for i in range(k):
            lambda_t[i] = lamb[i*V+j]
        psi_lam = psi_vec(lambda_t)

        for n in range(N):
            phi_lam_frac = phi[(n*k):((n+1)*k)]
            phi_lam_term += sum(vector_prod(phi_lam_frac, psi_lam))
    
    lb = term1 + term2 + phi_gam_term + phi_lam_term - entropy_theta - entropy_beta

    return lb

######################## 데이터 변환 ########################

# 데이터 프레임을 id로 매핑해서 내보냄
def make_id(df):
    df['movie_mapping'] = df['movie_id'].astype('category').cat.codes
    df['user_mapping'] = df['user_name'].astype('category').cat.codes

    user_map_info = df[['user_name', 'user_mapping']].drop_duplicates().sort_values('user_mapping')
    movie_map_info = df[['movie_id', 'movie_mapping']].drop_duplicates().sort_values('movie_mapping')

    df.drop(['movie_id', 'user_name'], axis = 1, inplace=True)

    return {
        'new_df': df,
        'movie_info': movie_map_info,
        'user_info': user_map_info
    }

def df2triplet(dict):                 
    df = dict['new_df']
    triplet = {}
    triplet['users'] = df['user_mapping']
    triplet['movies'] = df['movie_mapping']
    triplet['like'] = df['like']

    user_info = dict['user_info']
    movie_info = dict['movie_info']

    triplet['nrow'] = len(user_info)
    triplet['ncol'] = len(movie_info)
    
    triplet['user_info'] = user_info
    triplet['movie_info'] = movie_info

    return triplet

######################## 추천 ########################

# 상위 n개의 인덱스 가져오기
def get_top_indices(arr, top_n):
    # (인덱스, 값) 형태로 정렬
    sorted_indices = sorted(enumerate(arr), key=lambda x: x[1], reverse=True)
    # 상위 top_n개의 인덱스만 추출
    top_indices = [index for index, value in sorted_indices[:top_n]]
    return top_indices

# 추천하고자 하는 사용자 인덱스와 그 유저가 평가한 영화 찾기
def find_user(train, string):
    user_info = train['user_info']
    users = train['users']

    # target 유저
    user_idx = int(user_info[user_info['user_name'] == string]['user_mapping'])

    # target user가 평가한 영화의 인덱스 찾기
    df_idx = list(users[users == user_idx].index)
    movies = train['movies']
    rated_movies = []

    for idx in df_idx:
        rated_movies.append(movies[idx])

    return {
        'target': user_idx,
        'rated_movies': rated_movies
    }

def recommend(lda_result, train, n_recommend, string):      # 추천 함수 결과, triplet, 추천의 개수, user_name
    print(f'{string}에 대한 추천을 시작합니다')
    find = find_user(train, string)

    target_user = find['target']
    rated_movies = find['rated_movies']

    theta = lda_result['theta']
    beta = lda_result['beta']

    prediction_matrix = np.matmul(theta, beta)              # M by V matrix

    target_prob = prediction_matrix[target_user]

    for idx in rated_movies:
        target_prob[idx] = 0                                # 이미 평가한 영화는 0으로

    # 매핑된 영화 id를 원래 영화 id로 바꿔주기
    movie_info = train['movie_info']
    indices = get_top_indices(target_prob, n_recommend)
    recommend = []
    for idx in indices:
        movie_to_recommend = int(movie_info[movie_info['movie_mapping'] == idx]['movie_id'])
        recommend.append(movie_to_recommend)

    return recommend

######################## Latent Dirichlet Allocation ########################

def lda(triplet, n_topic, max_iterations=1000, eps=1e-5):
    users = triplet['users']
    movies = triplet['movies']
    like = triplet['like']

    M = triplet['nrow']
    V = triplet['ncol']
    k = n_topic

    temp_df = pd.concat([users, movies, like], axis=1)
    user_likes = temp_df.groupby('user_mapping')['like'].sum()

    # 인덱스 설정
    end_idx = list(np.cumsum(vector_int_prod(user_likes, k)))
    start_idx = [0] + end_idx[:len(end_idx)-1]

    liked_item = []

    for d in range(M):
        liked_item.append(list(temp_df[(temp_df['user_mapping'] == d) & (temp_df['like'] == 1)]['movie_mapping'].values))

    item_likes = temp_df.groupby('movie_mapping')['like'].sum()

    N = sum(item_likes)

    phi = [0] * (N * k)
    gamma = np.random.uniform(0, 1, M * k)
    lambd = np.random.uniform(0, 1, k * V)

    alpha = [0.1] * k
    eta = [0.1] * V

    LB = computeLB(alpha, eta, phi, gamma, lambd, M, k, V)

    iteration = 0

    while True:
        iteration += 1
        if iteration == max_iterations:
            print('max iteration reached')

        ## E-step
        phi_new = [0] * (N * k)
        gamma_new = np.random.uniform(0, 1, M * k)
        lambda_new = np.random.uniform(0, 1, k * V)
        ### 여기서부터 인덱스 잘 보기 ###
        for i in range(k):
            lambd[(i*V):((i+1)*V-1)] = psi_vec(lambd[(i*V):((i+1)*V-1)])
        
        for d in range(M):
            if int(user_likes[d]) != 0:
                nd = int(user_likes[d])
                ids = liked_item[d]
                current_phi = [0] * (nd * k)
                for l in range(nd):
                    for i in range(k):
                        current_phi[l*k+i] = lambd[i*V+ids[l]]
                
                current_gamma = gamma[(d*k):((d+1)*k-1)]

                psi_gamma = psi_vec(current_gamma)
                
                for l in range(nd):
                    opt_phi = vector_sum(current_phi[(l*k):((l+1)*k-1)], psi_gamma)
                    norm_phi = logsumexp(opt_phi)

                    current_phi[(l*k):((l+1)*k-1)] = np.exp(vector_int_sum(opt_phi, -norm_phi))
                
                phi_new[start_idx[d]:end_idx[d]] = current_phi

                phi_gamma = np.array(current_phi).reshape(nd, k)
                gamma_new[(d*k):((d+1)*k)] = np.sum(phi_gamma, axis=0) + alpha

                for l in range(nd):
                    for i in range(k):
                        lambda_new[i*V+ids[l]] = lambda_new[i*V+ids[l]] + current_phi[l*k+i]
        
        for i in range(k):
            lambda_new[(i*V):((i+1)*V-1)] = vector_sum(lambda_new[(i*V):((i+1)*V-1)], eta)
        
        LB_new = computeLB(alpha, eta, phi_new, gamma_new, lambda_new, M, k, V)

        critic = abs((LB-LB_new)/LB)

        if iteration % 50 == 0:
            print(f'{iteration} iterations, LB difference: {round(critic, 5)}')
        
        if (critic < eps) or (iteration >= max_iterations):
            break
     
        phi = phi_new
        gamma = gamma_new
        lambd = lambda_new
        LB = LB_new
    gamma_mat = gamma_new.reshape(M, k)
    lambda_mat = lambda_new.reshape(k, V)

    theta = [[0]*k for _ in range(M)]
    beta = [[0]*V for _ in range(k)]

    for d in range(M):
        psi_gamma = psi_vec(gamma_mat[d])
        norm_theta = logsumexp(psi_gamma)
        theta[d] = np.exp(vector_int_sum(psi_gamma, -norm_theta))

    for i in range(k):
        psi_lambda = psi_vec(lambda_mat[i])
        norm_lambda = logsumexp(psi_lambda)
        beta[i] = np.exp(vector_int_sum(psi_lambda, -norm_lambda))
    
    return {
        'phi': phi_new,
        'gamma': gamma_mat,
        'lambda': lambda_mat,
        'theta': theta,
        'beta': beta,
        'ELBO': LB_new,
        'iter':iteration
    }