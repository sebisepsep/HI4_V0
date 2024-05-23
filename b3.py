import numpy as np 
import matplotlib.pyplot as plt


kappa = np.load("kappa.npy")
flag = np.load("flag.npy")
"""elemente einladen"""

def x_vec(x):
    return np.array([x**i for i in range(2)])# x_0=1, x_1 = x

theta_vec = np.ones(2)
m = len(kappa)

def h_theta(theta,x):
    return 1/(1+np.exp(-np.dot(theta,x_vec(x))))

def cost(m, theta, x, y): #take care for different features
    term1 = y*np.log(h_theta(theta,x)) #should output an array - take care that it works with h(x)!
    term2 = (1-y)*np.log(1-h_theta(theta,x))
    return -1/m * sum(term1+term2) #dont need to calculate len(y) over and over again - rather use it as an input

def cost_derivative(m, j, theta, x, y):
    return -1/m*sum(y-h_theta(theta,x)*x_vec(x)[j])#might be inefficient, becasue I calculate every x_j in every step

#for linear minimalization
def golden(f,mini,mid,maxi,acc):
    # for test
    x_array = np.array([[None],[None],[None]]) #independ of dim - just for checking
    count = 0
    while True: 
        
        # step 1
        interval_1 = abs(maxi - mid)
        interval_2 = abs(mid - mini)

        if interval_1 > interval_2:
            larger_interval = (mid, maxi)
            x = maxi

        else:
            larger_interval = (mini, mid)
            x = mini
        
        #also for later!
        x_array[count%3] = x
        if (x_array[0]==x_array[1]) and (x_array[0]==x_array[2]):
            print("error in golden")
            value = x
            break
        #print(x_array)
        
        
        w = 0.38197 #golden ratio
        d = mid + (x-mid)*w
        
        print(abs(maxi - mini))
        # step 2
        if abs(maxi - mini) < acc:
            if f(d) < f(mid):
                print(f"d it is!. d = {d}")
                #print("a",mini)
                #print("b",mid)
                #print("c",maxi)
                value = d
                break
            else: 
                print(f"b it is!. b = {mid}")
                #print("a",mini)
                #print("c",maxi)
                #print("d",d)
                value = mid
                break

        # step 3
        #tighten towards d
        if f(d) < f(mid): 
            if mid < d < maxi: #b and c must be ordered :)
                mini,mid = mid,d

            else:
                maxi, mid = mid ,d

        #step 4
        #tighten towads b
        if f(d) > f(mid): 
            if mid < d < maxi:
                maxi = d

            else:
                mini = d
        count += 1
    return value

def opti_cost(lam):
    return cost(m, lam * theta_global, x_array_global, y_array_global)
"""global defined - not sure whether it is the best option"""


g = np.array([],dtype=object)
n_glob = np.array([],dtype=object)
gamma = np.array([])
lam_track = np.array([])

j_track = np.array([])

maxi = 1 #guess - but bracketing might be better...

theta_vec = np.ones(2)
m = len(kappa)

x_array_global = kappa.copy() #necessary?
y_array_global = flag.copy() #necessary?_


i = 0
while True:
    theta_global = theta_vec 
    
    g = np.append(g, 0)
    print(i)
    #calculate the direction of steepes decent for an initial point
    g_new = - np.array([cost_derivative(m, j, theta_vec, x_array_global, y_array_global) for j in range(2)])
    print("g_new",g_new)
    """take care of dimensions!!"""
    g[i] = g_new


    if i == 0:
        gamma = np.append(gamma,0)
        n_glob = np.append(n_glob, 0)

        #set new direction
        n_glob[0] = g[0] #n[i-1] nicht da und gamma_i = 0



    else: 
        #else calculate gamma_i
        gamma_val = np.dot((g[i]-g[i-1]),g[i])/sum(g[i-1]**2) #gamma_i is a scalar, g_i is a vector - this was very inefficient before...
        gamma = np.append(gamma,gamma_val)

        #set new direction
        n_val = g[i]+gamma[i]*n_glob[i-1]  
        n_glob = np.append(n_glob, 0)
        n_glob[i] = n_val

    mini = 0
    #now do line minimization to find lambda for new x point via golden ratio search
    #because of gradient I would guess itstarts at zero!
    if i>2:
        lam_min_nacher = lam_track[i-1]
        lam_min_vorher = lam_track[i-2]

        if lam_min_vorher == lam_min_nacher:
            maxi = maxi*0.5

    mid = mini +  (maxi-mini)*0.5

    #provide me with the minimum
    """need function that finds my bracket"""
    # golden ratio search assumes that in the bracket is a minimum
    
    lam_min = golden(opti_cost,mini,mid,maxi,10**-4)

    lam_track = np.append(lam_track, lam_min)
    
    theta_before = theta_vec

    #calculate new parameter
    theta_vec = theta_vec+lam_min*n_glob[i]

    #new parameter
    theta_after = theta_vec #initial only for initial initial conditions...
    
    """you can also use the previous calculation - makes it faster"""
    a1 = cost(m, theta_after, x_array_global, y_array_global)
    a2 = cost(m, theta_before, x_array_global, y_array_global)
    
    j_track = np.append(j_track, 0)
    j_track[-1] = a1
    
    print("i",i)
    #check for convergance by comparing to its target accuracy
    if i>2:
        check = 2*abs(a1 - a2)/abs(a1+a2)

        print("check",check)
        print(f"currently theta:{theta_after}")

        if check < 10**-6: #I changed this part
            print("reached target accuracy")
            print(f"theta:{theta_after} it is")
            break 

    i += 1

plt.plot(j_track)
plt.xlabel("Iterations")
plt.ylabel("J(theta)")
plt.savefig("3b_fig.jpg")