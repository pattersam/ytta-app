import { ILabelOccurance, IUserProfile, IVideo } from '@/interfaces';
import { MainState, AppNotification } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';


export const mutations = {
    setToken(state: MainState, payload: string) {
        state.token = payload;
    },
    setLoggedIn(state: MainState, payload: boolean) {
        state.isLoggedIn = payload;
    },
    setLogInError(state: MainState, payload: boolean) {
        state.logInError = payload;
    },
    setUserProfile(state: MainState, payload: IUserProfile) {
        state.userProfile = payload;
    },
    setDashboardMiniDrawer(state: MainState, payload: boolean) {
        state.dashboardMiniDrawer = payload;
    },
    setDashboardShowDrawer(state: MainState, payload: boolean) {
        state.dashboardShowDrawer = payload;
    },
    addNotification(state: MainState, payload: AppNotification) {
        state.notifications.push(payload);
    },
    removeNotification(state: MainState, payload: AppNotification) {
        state.notifications = state.notifications.filter((notification) => notification !== payload);
    },
    setUserVideos(state: MainState, payload: IVideo[]) {
        state.userVideos = payload;
    },
    setNewVideo(state: MainState, payload: IVideo) {
        state.newVideo = payload;
    },
    setUserLabelOccurances(state: MainState, payload: ILabelOccurance[]) {
        const labelOccurances: {[name: string]: ILabelOccurance } = {};
        for (const lo of payload) {
            const name = lo.label_name;
            if (!(name in labelOccurances)) {
                labelOccurances[name] = lo;
                labelOccurances[name].num_videos = 0;
            } else {
                labelOccurances[name].avg_confidence = (
                    (
                        labelOccurances[name].avg_confidence * labelOccurances[name].num_occurances
                      + lo.avg_confidence * lo.num_occurances
                    ) / (labelOccurances[name].num_occurances + lo.num_occurances)
                    );
                labelOccurances[name].num_occurances += lo.num_occurances;
            }
            labelOccurances[name].num_videos++;
            }
        state.userLabelOccurances = Object.values(labelOccurances);
    },
};

const {commit} = getStoreAccessors<MainState | any, State>('');

export const commitSetDashboardMiniDrawer = commit(mutations.setDashboardMiniDrawer);
export const commitSetDashboardShowDrawer = commit(mutations.setDashboardShowDrawer);
export const commitSetLoggedIn = commit(mutations.setLoggedIn);
export const commitSetLogInError = commit(mutations.setLogInError);
export const commitSetToken = commit(mutations.setToken);
export const commitSetUserProfile = commit(mutations.setUserProfile);
export const commitAddNotification = commit(mutations.addNotification);
export const commitRemoveNotification = commit(mutations.removeNotification);
export const commitSetUserVideos = commit(mutations.setUserVideos);
export const commitSetNewVideo = commit(mutations.setNewVideo);
export const commitSetUserLabelOccurances = commit(mutations.setUserLabelOccurances);

