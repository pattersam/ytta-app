import { MainState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    hasAdminAccess: (state: MainState) => {
        return (
            state.userProfile &&
            state.userProfile.is_superuser && state.userProfile.is_active);
    },
    loginError: (state: MainState) => state.logInError,
    dashboardShowDrawer: (state: MainState) => state.dashboardShowDrawer,
    dashboardMiniDrawer: (state: MainState) => state.dashboardMiniDrawer,
    userProfile: (state: MainState) => state.userProfile,
    token: (state: MainState) => state.token,
    isLoggedIn: (state: MainState) => state.isLoggedIn,
    firstNotification: (state: MainState) => state.notifications.length > 0 && state.notifications[0],
    userVideos: (state: MainState) => state.userVideos,
    userLabelOccurances: (state: MainState) => state.userLabelOccurances,
    userLabelOccuranceGraphNodes: (state: MainState) => {
        const nodes: Array<{}> = [];
        for (const lo of state.userLabelOccurances) {
            if (lo.num_occurances < 5) {
                continue;
            }
            nodes.push({id: lo.label_name, name: lo.label_name, _size: lo.num_occurances});
        }
        return nodes;
    },
    userLabelOccuranceGraphLinks: (state: MainState) => {
        const linksDrawn: string[] = [];
        const links: Array<{}> = [];
        let vids: number[];
        for (const slo of state.userLabelOccurances) {
            if (slo.num_occurances < 5) {
                continue;
            }
            for (const tlo of state.userLabelOccurances) {
                if (tlo.num_occurances < 5) {
                    continue;
                }
                if (slo.label_name === tlo.label_name) {
                    continue;
                }
                if (
                    linksDrawn.includes(slo.label_name + '|' + tlo.label_name)
                    || linksDrawn.includes(tlo.label_name + '|' + slo.label_name)
                ) {
                    continue;
                }
                vids = (slo.video_ids ?? []).filter((value) => (tlo.video_ids ?? []).includes(value));
                if (vids.length === 0) {
                    continue;
                } else {
                    links.push({sid: slo.label_name, tid: tlo.label_name});
                    linksDrawn.push(slo.label_name + '|' + tlo.label_name);
                }
            }
        }
        return links;
    },
};

const {read} = getStoreAccessors<MainState, State>('');

export const readDashboardMiniDrawer = read(getters.dashboardMiniDrawer);
export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readHasAdminAccess = read(getters.hasAdminAccess);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);
export const readUserVideos = read(getters.userVideos);
export const readUserLabelOccurances = read(getters.userLabelOccurances);
export const readUserLabelOccuranceGraphNodes = read(getters.userLabelOccuranceGraphNodes);
export const readUserLabelOccuranceGraphLinks = read(getters.userLabelOccuranceGraphLinks);
