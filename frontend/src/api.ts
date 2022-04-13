import axios, { AxiosPromise } from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate, IVideo, ILabelOccurance } from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

async function _getUserLabelOccurances(
  token: string,
  userId: number,
  cursor: number = 0,
  limit: number = 1000,
  data: ILabelOccurance[] = [],
  ): Promise<ILabelOccurance[]> {
  return axios.get<ILabelOccurance[]>(
    `${apiUrl}/api/v1/users/${userId}/label_occurances`,
    Object.assign(
      { params: {
        with_label_names: true,
        skip: cursor,
        limit,
      } },
      authHeaders(token),
    ),
  )
  .then((response) => {
    if (response.data.length < 1 ) {
      return data;
    }
    data.push(...response.data);
    if (response.data.length < limit ) {
      return data;
    }
    return _getUserLabelOccurances(
      token,
      userId,
      cursor = cursor + response.data.length,
      limit = limit,
      data = data,
      );
});
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async getUserVideos(token: string, userId: number) {
    return axios.get<IVideo[]>(`${apiUrl}/api/v1/users/${userId}/videos`, authHeaders(token));
  },
  async createVideo(token: string, url: string) {
    return axios.post(`${apiUrl}/api/v1/videos/`, {url}, authHeaders(token));
  },
  async deleteVideo(token: string, id: number) {
    return axios.delete(`${apiUrl}/api/v1/videos/${id}`, authHeaders(token));
  },
  async getUserLabelOccurances(token: string, userId: number) {
    return _getUserLabelOccurances(token, userId);
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
};
