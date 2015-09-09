--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY auth_group (id, name) FROM stdin;
4	CURATOR
2	DIL
1	READ
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('auth_group_id_seq', 4, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: prem
--

--COPY django_content_type (id, app_label, model) FROM stdin;
--1	admin	logentry
--2	auth	permission
--3	auth	group
--4	auth	user
--5	contenttypes	contenttype
--6	sessions	session
--7	authtoken	token
--8	pydgin_auth	userprofile
--9	pydgin_auth	globalpermission
--10	auth_test	authtestpermission
--38	elastic	gene_elastic_permission
--39	elastic	marker_elastic_permission
--40	elastic	publication_elastic_permission
--\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY auth_permission (id, name, codename, content_type_id) FROM stdin;
31	Can read only	can_read	9
32	Can read auth test data	can_read	10
33	Can read curate data	can_read_curate	10
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
4	4	33
6	2	32
15	1	31
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 15, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('auth_permission_id_seq', 38, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
5	pbkdf2_sha256$20000$oGNfCvP92wP6$kp32dEh7L34czRF+t4e7cZ4JgXEn4GhvBn3rIY1crnE=	2015-08-04 17:20:32.689239+01	f	prem_dil			prem.apa@gmail.com	f	t	2015-07-22 13:09:28+01
3	pbkdf2_sha256$20000$T02Ktf3IpbhF$2ZiXuYHYAtNiLQkrmiiZUwJmPsb4mtGV4kzc/+5WVAE=	2015-08-05 09:26:56.360424+01	f	prem_ro			prem.apa@gmail.com	f	t	2015-07-22 11:33:35.424898+01
6	pbkdf2_sha256$20000$Ba1MF9jdjCLF$WuC075BcgzkrAf4ShVGgZO6FviNYlnfEngOF4za9L6k=	2015-07-30 15:16:57.951831+01	f	prem_curator			prem.apa@gmail.com	f	t	2015-07-22 13:10:15+01
10	pbkdf2_sha256$20000$Wi2WC2wYikwm$oDDuxs9iLOSw+F5PGouyMmN6vib37jafNgotOD9IOcw=	2015-07-31 14:18:28.307727+01	f	dummyuser			dummy@dummy.com	f	t	2015-07-31 14:18:28.194449+01
11	pbkdf2_sha256$20000$StXVdtds49Of$wHQLXChZs/5SauBZHhboaVjoFHlYx7+0h16ih04LK1M=	2015-07-31 14:20:53.518653+01	f	testuser			test@testmail.com	f	t	2015-07-31 14:20:53.413251+01
1	pbkdf2_sha256$20000$WB0wuebUGDZT$RDeQG/w6ahCfEZ8pUaIsFbz0KLa1l3uM48s6uUPPhCY=	2015-08-04 16:38:40.12695+01	t	admin			premanand.achuthan@cimr.cam.ac.uk	t	t	2015-07-22 11:15:09.182062+01
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
2	3	1
8	6	1
9	6	4
10	5	1
11	5	2
15	10	1
16	11	1
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 16, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('auth_user_id_seq', 11, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY authtoken_token (key, created, user_id) FROM stdin;
f78a60ebe895d81199430d33fd05ca01c6d8557c	2015-07-24 15:56:55.671414+01	3
66d6ede5ab498afa052f2deb4552ffb56c612798	2015-07-24 15:59:01.600009+01	5
ee2a620269a19eeecff1a01d95c66b7f50b9fd2d	2015-07-31 14:18:28.252227+01	10
ceb7f8da042cdfb3df4a829ad28c59ee577f5132	2015-07-31 14:20:53.465311+01	11
fa9d3023e0a31cc6bd40ddb0cf337ebbcf176974	2015-07-31 14:20:53.469208+01	6
76f82eafbd169a0676220fdacbb13b706f4be81b	2015-07-31 14:20:53.474583+01	1
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: prem
--

--COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
--1	2015-07-22 11:20:14.771839+01	28	pydgin_auth | global_permission | Can read only	1		2	1
--2	2015-07-22 11:24:20.869202+01	1	READ	1		3	1
--3	2015-07-22 11:24:29.822029+01	2	DIL	1		3	1
--4	2015-07-22 11:24:55.079537+01	3	PYDGIN_ADMIN	1		3	1
--5	2015-07-22 11:25:11.745195+01	4	CURATOR	1		3	1
--6	2015-07-22 11:33:06.780943+01	2	prem_ro	3		4	1
--7	2015-07-22 11:43:16.5422+01	1	READ	2	Changed permissions.	3	1
--8	2015-07-22 14:11:39.82382+01	4	prem_admin	2	Changed groups.	4	1
--9	2015-07-22 14:12:08.755597+01	6	prem_curator	2	Changed groups.	4	1
--10	2015-07-22 14:12:30.81386+01	5	prem_dil	2	Changed groups.	4	1
--11	2015-07-23 09:27:04.695959+01	32	auth_test | auth_test_permissions | Can read auth test data	1		2	1
--12	2015-07-23 09:39:32.926732+01	1	READ	2	Changed permissions.	3	1
--13	2015-07-23 10:34:02.049041+01	33	auth_test | auth_test_permissions | Can read curate data	1		2	1
--14	2015-07-23 10:34:57.614746+01	4	CURATOR	2	Changed permissions.	3	1
--15	2015-07-23 11:12:13.308813+01	1	READ	2	Changed permissions.	3	1
--16	2015-07-23 11:13:59.646979+01	2	DIL	2	Changed permissions.	3	1
--17	2015-07-23 16:18:34.374252+01	34	auth_test | auth_test_perms | Test perm for auth_test	1		2	1
--18	2015-07-23 16:18:57.902068+01	34	auth_test | auth_test_perms | Test perm for auth_test	3		2	1
--19	2015-07-29 17:45:09.065258+01	35	elastic | gene_elastic_permission | elastic	1		38	1
--20	2015-07-29 17:46:09.502255+01	35	elastic | gene_elastic_permission | can_read_gene_elastic	2	Changed name.	38	1
--21	2015-07-29 17:46:42.55436+01	36	elastic | marker_elastic_permission | can_read_marker_elastic	1		39	1
--22	2015-07-30 10:27:11.423342+01	37	elastic | publication_elastic_permission | can_read_publication_elastic	1		40	1
--23	2015-07-30 10:29:26.293395+01	1	READ	2	Changed permissions.	3	1
--24	2015-07-30 11:18:24.489946+01	1	READ	2	Changed permissions.	3	1
--25	2015-07-30 11:18:58.670571+01	35	elastic | gene_elastic_permission | can_read_gene_elastic	3		38	1
--26	2015-07-30 11:19:06.716747+01	37	elastic | publication_elastic_permission | can_read_publication_elastic	3		40	1
--27	2015-07-30 12:05:36.859836+01	1	READ	2	Changed permissions.	3	1
--28	2015-07-30 13:35:03.556592+01	1	READ	2	Changed permissions.	3	1
--29	2015-07-30 13:37:13.89116+01	38	elastic | gene_elastic_permission | can_read_gene_elastic	1		38	1
--30	2015-07-30 13:38:12.246409+01	38	elastic | gene_elastic_permission | can_read_gene_elastic	3		38	1
--31	2015-07-30 13:38:34.07787+01	1	READ	2	Changed permissions.	3	1
--32	2015-07-31 12:15:56.090238+01	7	dummyuser	3		4	1
--33	2015-07-31 14:17:47.081649+01	8	dummyuser	3		4	1
--34	2015-07-31 14:17:47.085132+01	9	testuser	3		4	1
--35	2015-08-03 09:38:47.338476+01	4	prem_admin	3		4	1
--36	2015-08-03 09:39:04.215341+01	3	PYDGIN_ADMIN	3		3	1
--\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

--SELECT pg_catalog.setval('django_admin_log_id_seq', 36, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('django_content_type_id_seq', 15, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: prem
--

--COPY django_migrations (id, app, name, applied) FROM stdin;
--1	contenttypes	0001_initial	2015-07-22 11:05:57.812959+01
--2	auth	0001_initial	2015-07-22 11:05:58.008828+01
--3	admin	0001_initial	2015-07-22 11:05:58.060693+01
--4	sessions	0001_initial	2015-07-22 11:08:16.285183+01
--5	authtoken	0001_initial	2015-07-22 11:08:27.30499+01
--6	pydgin_auth	0001_initial	2015-07-22 11:08:41.384331+01
--7	auth_test	0001_initial	2015-07-23 09:21:56.225542+01
--8	auth_test	0002_auto_20150723_0920	2015-07-23 09:21:56.23793+01
--9	pydgin_auth	0002_userprofile_is_terms_agreed	2015-07-31 12:00:26.157489+01
--\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

--SELECT pg_catalog.setval('django_migrations_id_seq', 9, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: prem
--

--COPY django_session (session_key, session_data, expire_date) FROM stdin;
--v8frh5ipqx3uzx6y2zlcuiv33zewfp2d	ZTU0ZTU5N2FlYTE0MDhkM2FkOGMwMzUyODFhYjFmNjNhY2NlNWI1NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiI1OTcwZmMyODdhNTZmZjAxNzc2Yjg3NjU3YjIyODgzNTAxOTI4OTdhIn0=	2015-08-17 09:36:14.49557+01
--q9x43xfbq4jq8vx3pvgfih7mfj643mjo	OThiZWVkODA0NjIwYTEyM2E1ZjdmMTc4ZjZkMGVhZTk3ZDhiZmU2Yjp7Il9hdXRoX3VzZXJfaGFzaCI6ImNhZDY1OTIwMjMxMWRiZGY0NjU5MzlhZjg2NDg2OWI5NTczYmY3YTYiLCJfYXV0aF91c2VyX2lkIjoiMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=	2015-08-05 13:41:25.603426+01
--hsoh3xaqelecbi5xsy1k1cbpwulhr6gc	ZWNjM2UwYWYzZmMwZmRjMjBlNzIyYTlmZmRiOTcwMTk3MDcxOTNkZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjYiLCJfYXV0aF91c2VyX2hhc2giOiJiM2IwN2M4Mjk4Yjk2OGE5ZGZiM2I3ZTU3YTcwOTA4YjY0NjhmMjUxIn0=	2015-08-06 14:51:32.202745+01
--t06415dq2y7i4m5cq44fv6fy4enau6mc	NDY4MjBiY2ZlZWQ1NWZhMThmYzI4NzJlYmFkODJhYzczYWUzNmMyZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjU5NzBmYzI4N2E1NmZmMDE3NzZiODc2NTdiMjI4ODM1MDE5Mjg5N2EiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=	2015-08-13 15:20:37.047965+01
--p8dp6avlyube38aeu1vqfgkp5ef1x3x0	MGY5NGViY2EyY2Y1NDZiMzAzMjY5M2E0NTBlMmFlMDZmNzc1ZDYxNTp7Il9hdXRoX3VzZXJfaGFzaCI6ImY0Yzc3MGQxM2RiMWNlNzlhMDJlYjNlOWJkYTlmNmEyMzE4ZTZmZmIiLCJfYXV0aF91c2VyX2lkIjoiNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=	2015-08-07 15:59:01.570484+01
--\.


--
-- Data for Name: pydgin_auth_userprofile; Type: TABLE DATA; Schema: public; Owner: prem
--

COPY pydgin_auth_userprofile (id, user_id, is_terms_agreed) FROM stdin;
1	3	f
3	5	f
4	6	f
7	1	f
9	10	t
10	11	t
\.


--
-- Name: pydgin_auth_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prem
--

SELECT pg_catalog.setval('pydgin_auth_userprofile_id_seq', 10, true);


--
-- PostgreSQL database dump complete
--

