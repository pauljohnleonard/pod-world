TIME_LIMIT=40.0
TRIPS_LIMIT=60.0

def evaluate(pod):

    if pod.state.age > TIME_LIMIT:
        dist=pod.state.pos_trips-pod.state.neg_trips
        mess=" Time limit. Trips wires crossed ="+str(dist)
        score=dist
        pod.stat='T'
        return score,True,mess

    if pod.state.pos_trips - pod.state.neg_trips >= TRIPS_LIMIT:
        mess=" Success age="+str(pod.state.age)
        score=TRIPS_LIMIT + (TIME_LIMIT-pod.state.age)
        pod.stat='S'
        return score,True,mess



    if pod.state.collide:
        dist=pod.state.pos_trips-pod.state.neg_trips+pod.state.seg_pos
        age=pod.state.age
        mess=" Crashed age="+str(age)+" progress ="+str(dist)
        score=dist
        pod.stat='C'
        return score,True,mess

    dist=pod.state.pos_trips-pod.state.neg_trips
    score=dist
    pod.stat='R'
    return score,False,""


